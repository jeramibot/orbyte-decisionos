"""Pure, deterministic arithmetic. Estimated inputs are never treated as forecasts."""
from decimal import Decimal, ROUND_HALF_UP


def D(value):
    n = Decimal(str(value))
    if not n.is_finite():
        raise ValueError("Inputs must be finite numbers")
    return n


def coverage(quantity, daily_usage):
    q, u = D(quantity), D(daily_usage)
    if q < 0 or u < 0:
        raise ValueError("Stock and daily usage cannot be negative")
    return q / u if u else None


def evaluate(context):
    item = context["item"]
    q, usage, threshold, purchase = [D(item[k]) for k in ("quantity", "daily_usage", "threshold_days", "purchase_quantity")]
    if threshold <= 0 or purchase <= 0:
        raise ValueError("Threshold and purchase quantity must be positive")
    days = coverage(q, usage)
    if days is None:
        raise ValueError("Daily usage is zero; enter a positive estimate before evaluating procurement")
    options = []
    for offer in context["offers"]:
        price, lead = D(offer["unit_price_sen"]), D(offer["lead_days"])
        if price <= 0 or lead < 0:
            raise ValueError("Supplier price must be positive and lead time nonnegative")
        cost = int((price * purchase).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        gap = max(lead - days, Decimal(0))
        options.append({**offer, "total_sen": cost, "stockout_risk": lead > days,
            "stockout_gap_days": float(gap), "arrival_buffer_days": float(days - lead),
            "coverage_after_arrival_days": float((max(q - usage * lead, Decimal(0)) + purchase) / usage),
            "risk": f"Delivery exceeds stock coverage by {gap.normalize()} days" if gap else "Estimated delivery is within current stock coverage"})
    if not options:
        raise ValueError("No supplier offers available; request a synthetic quotation first")
    cheapest = min(o["total_sen"] for o in options)
    for o in options:
        o["premium_sen"] = o["total_sen"] - cheapest
    preferred = min(options, key=lambda o: (o["stockout_risk"], o["total_sen"], o["lead_days"]))
    return {"coverage_days": float(days), "threshold_days": float(threshold),
        "triggered": days < threshold, "purchase_quantity": float(purchase),
        "options": options, "suggested_offer_id": preferred["id"],
        "assumptions": ["Daily consumption remains constant at the entered estimate.",
            "Supplier delivery times are estimates, not guarantees.",
            "Prices exclude unprovided shipping, tax and discounts.",
            "No other incoming stock, waste or spoilage is included."],
        "missing_information": ["Shelf life and storage capacity for the proposed purchase", "Delivery guarantees and additional charges"],
        "explanation": "Prefer an offer arriving within estimated stock coverage, then the lowest quoted total. Owner makes the final choice."}
