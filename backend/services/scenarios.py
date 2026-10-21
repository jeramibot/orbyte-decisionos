"""Small reusable synthetic scenarios. Descriptions are inputs, never generated findings."""


def build_scenario(request, context):
    question = (f"What operational and customer-service complications could emerge if ingredient delivery is delayed by {request.delay_days} days?"
        if request.template == "delivery_delay" else
        f"What stakeholder concerns could arise from a hypothetical {request.price_change_percent}% café menu-price change?")
    return {"template": request.template, "question": question, "rounds": request.rounds, "context": context,
        "stakeholders": ["Business owner", "Purchasing manager", "Supplier representative", "Delivery coordinator", "Customer group"],
        "assumptions": ["All people and business records are fictional.", "Agent reactions are exploratory, not calibrated forecasts.",
            "No probabilities, predicted sales, demand forecasts or autonomous procurement decisions may be inferred."],
        "requested_sections": ["Stakeholder reactions", "Risks", "Mitigations", "Missing information", "Limitations"]}
