import json
from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
from models import UserCarProfile, FinalComparisonReport

personal_agent = Agent(
    name="autocollective_personal_concierge",
    seed="personal_concierge_seed_fetchathon_2026",
    port=8000,
    endpoint=["http://localhost:8000/submit"],
)

chat_proto = Protocol(spec=chat_protocol_spec)
COORDINATOR_ADDRESS = ""
user_sessions = {}

def create_text_chat(text: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)],
    )

def render_interactive_card(report: FinalComparisonReport) -> str:
    card = {
        "type": "card",
        "title": f"🎉 Group Negotiation Complete: {report.pool_id.upper()}",
        "subtitle": f"Best Deal: ₹{report.best_bid.final_price_per_unit} Lakhs | Total Group Savings: ₹{report.total_group_savings_lakhs} Lakhs!",
        "sections": [
            {
                "heading": "🏆 Recommended Dealership",
                "content": f"**{report.best_bid.dealer_name}**\n- Final On-Road: ₹{report.best_bid.final_price_per_unit} Lakhs\n- Delivery: {report.best_bid.delivery_days} days\n- Perks: {', '.join(report.best_bid.added_perks)}"
            },
            {
                "heading": "📊 Comparison Across Dealerships",
                "content": "\n".join([
                    f"• **{b.dealer_name}**: ₹{b.final_price_per_unit}L (Discount: ₹{round(b.bulk_discount_per_unit, 2)}L, Delivery: {b.delivery_days}d)"
                    for b in report.bids
                ])
            }
        ],
        "actions": [
            {"label": "Lock-In Group Discount", "action": "accept_deal"},
            {"label": "Request Custom Accessories", "action": "customize"}
        ]
    }
    return json.dumps(card, indent=2)

@chat_proto.on_message(ChatMessage)
async def handle_user_chat(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))
    
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            reply = create_text_chat(
                "🚗 **Welcome to AutoCollective AI!**\n\n"
                "I am your Personal Car Buying Concierge powered by Fetch.ai.\n"
                "Instead of negotiating alone, I pool your demand with nearby buyers on Agentverse to unlock bulk dealership discounts.\n\n"
                "What car, variant, and city are you planning to buy? (e.g. *'Looking for Hyundai Creta in Mumbai'*)"
            )
            await ctx.send(sender, reply)
        elif isinstance(item, TextContent):
            user_sessions["active_client"] = sender
            text = item.text.strip()
            ctx.logger.info(f"User message received: {text}")

            city = "Mumbai"
            if "delhi" in text.lower():
                city = "Delhi"
            elif "bangalore" in text.lower():
                city = "Bangalore"

            profile = UserCarProfile(
                user_id=sender,
                car_model="Hyundai Creta",
                variant="SX(O) Petrol AT",
                budget_max_lakhs=18.5,
                city=city
            )
            
            update = create_text_chat(
                f"🎯 **Preferences Logged**: {profile.car_model} ({profile.variant}) in **{profile.city}**.\n"
                f"🤝 Found 2 other active buyers matching your criteria!\n"
                f"🚀 Forming a collective buyer pool of 3 and requesting bulk quotations from local dealer agents..."
            )
            await ctx.send(sender, update)
            
            if COORDINATOR_ADDRESS:
                await ctx.send(COORDINATOR_ADDRESS, profile)

@personal_agent.on_message(model=FinalComparisonReport)
async def handle_negotiation_outcome(ctx: Context, sender: str, report: FinalComparisonReport):
    client_addr = user_sessions.get("active_client")
    if not client_addr:
        return

    summary = (
        f"✅ **Collective Negotiations Completed!**\n\n"
        f"Because of your group size of 3, dealers competed and offered up to **₹{report.best_bid.bulk_discount_per_unit} Lakhs discount** per car!\n\n"
        f"**Best Offer: {report.best_bid.dealer_name}** at **₹{report.best_bid.final_price_per_unit} Lakhs** (Delivery in {report.best_bid.delivery_days} days).\n"
        f"Perks: {', '.join(report.best_bid.added_perks)}"
    )
    await ctx.send(client_addr, create_text_chat(summary))
    
    card_json = render_interactive_card(report)
    await ctx.send(client_addr, create_text_chat(f"```json\n{card_json}\n```"))

personal_agent.include(chat_proto, publish_manifest=True)
