from decimal import Decimal
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field

Amount = Annotated[Decimal, Field(ge=0, le=1_000_000, decimal_places=3, allow_inf_nan=False)]
PositiveAmount = Annotated[Decimal, Field(gt=0, le=1_000_000, decimal_places=3, allow_inf_nan=False)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class MonitorRequest(StrictModel):
    item_id: str = Field(min_length=1, max_length=40)


class InventoryUpdate(StrictModel):
    quantity: Amount
    daily_usage: Amount
    threshold_days: Annotated[Decimal, Field(gt=0, le=365, decimal_places=3, allow_inf_nan=False)]
    purchase_quantity: PositiveAmount
    expected_version: int = Field(ge=1)
    reason: str = Field(min_length=3, max_length=500)


class OfferUpdate(StrictModel):
    unit_price_sen: int = Field(gt=0, le=100_000_000)
    lead_days: Annotated[Decimal, Field(ge=0, le=365, decimal_places=3, allow_inf_nan=False)]
    expected_version: int = Field(ge=1)
    reason: str = Field(min_length=3, max_length=500)


class Resolution(StrictModel):
    action: Literal["approve", "reject", "cancel"]
    option_id: str | None = Field(default=None, max_length=40)
    reason: str = Field(min_length=3, max_length=1000)
    acknowledge_risk: bool = False


class ScenarioRequest(StrictModel):
    template: Literal["delivery_delay", "price_change"] = "delivery_delay"
    item_id: str = Field(default="milk", max_length=40)
    delay_days: int = Field(default=3, ge=1, le=14)
    price_change_percent: int = Field(default=10, ge=-30, le=30)
    rounds: int = Field(default=2, ge=1, le=3)


class DecisionInsights(StrictModel):
    assumptions: list[str]
    stakeholder_reactions: list[str]
    risks: list[str]
    mitigations: list[str]
    missing_information: list[str]
    limitations: list[str]
    source_run_id: str
    report_id: str
    narrative: str
