from uagents import Agent, Context
from models import RequestForQuote, DealershipBid

dealer_metro = Agent(name="dealer_metro", seed="dealer_metro_secret_seed_2026_1", port=8001, endpoint=["http://localhost:8001/submit"])
dealer_apex = Agent(name="dealer_apex", seed="dealer_apex_secret_seed_2026_2", port=8002, endpoint=["http://localhost:8002/submit"])
dealer_star = Agent(name="dealer_star", seed="dealer_star_secret_seed_2026_3", port=8003, endpoint=["http://localhost:8003/submit"])

@dealer_metro.on_message(model=RequestForQuote)
async def quote_metro(ctx: Context, sender: str, rfq: RequestForQuote):
    base_price = 18.0
    # Aggressive volume discount formula
    discount = 0.30 + (0.15 * rfq.quantity)
    final = round(base_price - discount, 2)
    bid = DealershipBid(
        dealer_name="Metro Hyundai Hub",
        dealer_address=ctx.address,
        pool_id=rfq.pool_id,
        original_price=base_price,
        bulk_discount_per_unit=round(discount, 2),
        final_price_per_unit=final,
        delivery_days=14,
        added_perks=["7D Mats", "Extended 5-Year Warranty", "Ceramic Coating"]
    )
    ctx.logger.info(f"Metro Hyundai quoted ₹{bid.final_price_per_unit}L (Bulk discount: ₹{bid.bulk_discount_per_unit}L)")
    await ctx.send(sender, bid)

@dealer_apex.on_message(model=RequestForQuote)
async def quote_apex(ctx: Context, sender: str, rfq: RequestForQuote):
    base_price = 18.0
    discount = 0.20 + (0.10 * rfq.quantity)
    final = round(base_price - discount, 2)
    bid = DealershipBid(
        dealer_name="Apex Express Motors",
        dealer_address=ctx.address,
        pool_id=rfq.pool_id,
        original_price=base_price,
        bulk_discount_per_unit=round(discount, 2),
        final_price_per_unit=final,
        delivery_days=3,
        added_perks=["Express 3-Day Delivery", "Free 1st Year Service"]
    )
    ctx.logger.info(f"Apex Motors quoted ₹{bid.final_price_per_unit}L (Express Delivery)")
    await ctx.send(sender, bid)

@dealer_star.on_message(model=RequestForQuote)
async def quote_star(ctx: Context, sender: str, rfq: RequestForQuote):
    base_price = 18.0
    discount = 0.25 + (0.10 * rfq.quantity)
    final = round(base_price - discount, 2)
    bid = DealershipBid(
        dealer_name="Star City Auto",
        dealer_address=ctx.address,
        pool_id=rfq.pool_id,
        original_price=base_price,
        bulk_discount_per_unit=round(discount, 2),
        final_price_per_unit=final,
        delivery_days=7,
        added_perks=["Infotainment Upgrade", "Roadside Assistance"]
    )
    ctx.logger.info(f"Star City quoted ₹{bid.final_price_per_unit}L")
    await ctx.send(sender, bid)
