from uagents import Agent, Context
from models import UserCarProfile, RequestForQuote, DealershipBid, FinalComparisonReport
from typing import Dict, List

coordinator = Agent(name="collective_coordinator", seed="coordinator_secret_seed_2026_99", port=8004, endpoint=["http://localhost:8004/submit"])

DEALER_LIST: List[str] = []
pool_members: Dict[str, List[UserCarProfile]] = {}
pool_bids: Dict[str, List[DealershipBid]] = {}
client_mapping: Dict[str, str] = {}

REQUIRED_POOL_SIZE = 3

@coordinator.on_message(model=UserCarProfile)
async def on_user_profile(ctx: Context, sender: str, profile: UserCarProfile):
    pool_id = f"{profile.city}_{profile.car_model}".lower().replace(" ", "_")
    client_mapping[pool_id] = sender
    
    if pool_id not in pool_members:
        # Pre-seed 2 buyers to make live demo trigger instantly
        pool_members[pool_id] = [
            UserCarProfile(user_id="buyer_rahul", car_model=profile.car_model, variant=profile.variant, budget_max_lakhs=18.5, city=profile.city),
            UserCarProfile(user_id="buyer_priya", car_model=profile.car_model, variant=profile.variant, budget_max_lakhs=18.5, city=profile.city)
        ]

    pool_members[pool_id].append(profile)
    total_size = len(pool_members[pool_id])
    ctx.logger.info(f"Group pool '{pool_id}' reached {total_size}/{REQUIRED_POOL_SIZE} buyers!")

    if total_size >= REQUIRED_POOL_SIZE:
        ctx.logger.info(f"Pool capacity reached! Broadcasting Request For Quote to {len(DEALER_LIST)} dealers...")
        rfq = RequestForQuote(
            pool_id=pool_id,
            car_model=profile.car_model,
            variant=profile.variant,
            quantity=total_size,
            city=profile.city
        )
        pool_bids[pool_id] = []
        for dealer_addr in DEALER_LIST:
            await ctx.send(dealer_addr, rfq)

@coordinator.on_message(model=DealershipBid)
async def on_dealer_bid(ctx: Context, sender: str, bid: DealershipBid):
    p_id = bid.pool_id
    if p_id not in pool_bids:
        pool_bids[p_id] = []
    
    pool_bids[p_id].append(bid)
    ctx.logger.info(f"Dealer bid recorded from {bid.dealer_name} ({len(pool_bids[p_id])}/{len(DEALER_LIST)})")

    if len(pool_bids[p_id]) >= len(DEALER_LIST):
        sorted_bids = sorted(pool_bids[p_id], key=lambda b: b.final_price_per_unit)
        best = sorted_bids[0]
        total_savings = round(best.bulk_discount_per_unit * REQUIRED_POOL_SIZE, 2)
        
        report = FinalComparisonReport(
            pool_id=p_id,
            bids=sorted_bids,
            best_bid=best,
            total_group_savings_lakhs=total_savings
        )
        
        client_agent = client_mapping.get(p_id)
        if client_agent:
            ctx.logger.info(f"Delivering final comparison report to Personal Buyer Agent: {client_agent}")
            await ctx.send(client_agent, report)
