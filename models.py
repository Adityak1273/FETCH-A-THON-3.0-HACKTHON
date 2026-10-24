from pydantic import BaseModel
from typing import List, Optional

class UserCarProfile(BaseModel):
    user_id: str
    car_model: str
    variant: str
    budget_max_lakhs: float
    city: str

class RequestForQuote(BaseModel):
    pool_id: str
    car_model: str
    variant: str
    quantity: int
    city: str

class DealershipBid(BaseModel):
    dealer_name: str
    dealer_address: str
    pool_id: str
    original_price: float
    bulk_discount_per_unit: float
    final_price_per_unit: float
    delivery_days: int
    added_perks: List[str]

class FinalComparisonReport(BaseModel):
    pool_id: str
    bids: List[DealershipBid]
    best_bid: DealershipBid
    total_group_savings_lakhs: float
