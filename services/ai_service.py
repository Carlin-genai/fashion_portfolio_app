# Placeholder AI service — replace with real model integration.
def analyze_portfolio(portfolio, work_items):
    num_items = len(work_items)
    suggestions = []
    if num_items < 3:
        suggestions.append("Add more pieces to show variety (3+ recommended).")
    suggestions.append("Add materials & inspiration notes to strengthen storytelling.")
    return {
        "cohesion": 0.6,
        "color_balance": 0.7,
        "commercial_potential": 0.5,
        "presentation_score": 0.7,
        "suggestions": suggestions
    }
