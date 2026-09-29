"""
BuildWise AI - Verification Script for Dynamic Multi-Agent Outputs.
Tests Project A vs Project B across all 8 agents and verifies meaningful differentiation.
"""
from app.orchestration.state import ProjectState
from app.orchestration.graph import project_graph


def run_verification():
    # PROJECT A: 40 Lakh, 2 Bedrooms, 1 Floor, 30x40 Plot
    state_a = ProjectState(project_id=201, raw_input={
        "location": "Chennai",
        "plot_width": 30.0,
        "plot_length": 40.0,
        "plot_area": 1200.0,
        "number_of_floors": 1,
        "bedrooms": 2,
        "bathrooms": 2,
        "parking_required": True,
        "budget": 4000000.0,
        "architectural_style": "Modern",
        "construction_type": "RCC Frame",
        "target_completion_months": 8,
        "sustainability_priority": "Low",
        "special_requirements": "Single level home with compact garden"
    })

    res_a = project_graph.invoke(state_a)
    if isinstance(res_a, dict):
        res_a = ProjectState(**res_a)

    # PROJECT B: 60 Lakh, 4 Bedrooms, 2 Floors, 40x60 Plot
    state_b = ProjectState(project_id=202, raw_input={
        "location": "Chennai",
        "plot_width": 40.0,
        "plot_length": 60.0,
        "plot_area": 2400.0,
        "number_of_floors": 2,
        "bedrooms": 4,
        "bathrooms": 3,
        "parking_required": True,
        "budget": 6000000.0,
        "architectural_style": "Contemporary",
        "construction_type": "RCC Frame",
        "target_completion_months": 12,
        "sustainability_priority": "High",
        "special_requirements": "Rooftop solar and high acoustic insulation"
    })

    res_b = project_graph.invoke(state_b)
    if isinstance(res_b, dict):
        res_b = ProjectState(**res_b)

    print("================================================================================")
    print("                      BUILDWISE AI - DYNAMIC OUTPUT VERIFICATION                ")
    print("================================================================================")

    print("\n--- 1. PROJECT A: 40 Lakh | 2 BHK | 1 Floor | 30x40 Plot ---")
    print(f"Total Built-Up Area:     {res_a.design.total_built_up_area:,.1f} sq.ft (Carpet: {res_a.design.carpet_area:,.1f} sq.ft)")
    print(f"Floors Generated:        {len(res_a.design.floor_plan.floors)} Floor (G+0)")
    print(f"Total Rooms Generated:   {len(res_a.design.rooms)}")
    beds_a = [r.room_name for r in res_a.design.rooms if "bedroom" in r.room_name.lower()]
    print(f"Bedrooms ({len(beds_a)}):       {', '.join(beds_a)}")
    baths_a = [r.room_name for r in res_a.design.rooms if "bathroom" in r.room_name.lower()]
    print(f"Bathrooms ({len(baths_a)}):      {', '.join(baths_a)}")
    stair_a = [r.room_name for r in res_a.design.rooms if "staircase" in r.room_name.lower()]
    print(f"Staircase in 1-Floor:    {'Present (Warning!)' if stair_a else 'None (Correct - single floor!)'}")
    print(f"Turnkey Estimated Cost:  INR {res_a.cost.total_estimated_cost:,.2f} (@ INR {res_a.cost.cost_per_sqft:.0f}/sq.ft)")
    print(f"Budget Comparison:       {res_a.cost.budget_comparison['status']} (Variance: INR {res_a.cost.budget_comparison['variance']:,.2f})")
    print(f"Eco Material Rating:     {res_a.materials.overall_sustainability_rating}")
    print(f"Timeline Total:          {res_a.timeline.total_duration_months:.1f} Months ({len(res_a.timeline.phases)} CPM Tasks)")
    print(f"Overall Risk Level:      {res_a.risks.overall_risk_level} (Avg Score: {res_a.risks.average_risk_score:.1f})")
    print(f"Interior Scheme:         {res_a.interior.style_theme} ({len(res_a.interior.rooms)} spaces planned)")
    print(f"Finance Monthly EMI:     INR {res_a.finance.monthly_emi:,.2f} (Loan: INR {res_a.finance.loan_amount:,.2f})")

    print("\n--- 2. PROJECT B: 60 Lakh | 4 BHK | 2 Floors | 40x60 Plot ---")
    print(f"Total Built-Up Area:     {res_b.design.total_built_up_area:,.1f} sq.ft (Carpet: {res_b.design.carpet_area:,.1f} sq.ft)")
    print(f"Floors Generated:        {len(res_b.design.floor_plan.floors)} Floors (G+1)")
    print(f"Total Rooms Generated:   {len(res_b.design.rooms)}")
    beds_b = [r.room_name for r in res_b.design.rooms if "bedroom" in r.room_name.lower()]
    print(f"Bedrooms ({len(beds_b)}):       {', '.join(beds_b)}")
    baths_b = [r.room_name for r in res_b.design.rooms if "bathroom" in r.room_name.lower()]
    print(f"Bathrooms ({len(baths_b)}):      {', '.join(baths_b)}")
    stair_b = [r.room_name for r in res_b.design.rooms if "staircase" in r.room_name.lower()]
    print(f"Staircase in 2-Floor:    {'Present on both floors (Correct!)' if len(stair_b) == 2 else f'Count: {len(stair_b)}'}")
    print(f"Turnkey Estimated Cost:  INR {res_b.cost.total_estimated_cost:,.2f} (@ INR {res_b.cost.cost_per_sqft:.0f}/sq.ft)")
    print(f"Budget Comparison:       {res_b.cost.budget_comparison['status']} (Variance: INR {res_b.cost.budget_comparison['variance']:,.2f})")
    print(f"Eco Material Rating:     {res_b.materials.overall_sustainability_rating}")
    print(f"Timeline Total:          {res_b.timeline.total_duration_months:.1f} Months ({len(res_b.timeline.phases)} CPM Tasks)")
    print(f"Overall Risk Level:      {res_b.risks.overall_risk_level} (Avg Score: {res_b.risks.average_risk_score:.1f})")
    print(f"Interior Scheme:         {res_b.interior.style_theme} ({len(res_b.interior.rooms)} spaces planned)")
    print(f"Finance Monthly EMI:     INR {res_b.finance.monthly_emi:,.2f} (Loan: INR {res_b.finance.loan_amount:,.2f})")

    # Assertions
    assert len(beds_a) == 2, f"Expected 2 bedrooms for Project A, got {len(beds_a)}"
    assert len(beds_b) == 4, f"Expected 4 bedrooms for Project B, got {len(beds_b)}"
    assert len(res_a.design.floor_plan.floors) == 1, "Expected 1 floor for Project A"
    assert len(res_b.design.floor_plan.floors) == 2, "Expected 2 floors for Project B"
    assert len(stair_a) == 0, "Single floor should not have staircase"
    assert len(stair_b) == 2, "2-floor house should have staircase on both floors"
    assert res_a.cost.total_estimated_cost != res_b.cost.total_estimated_cost, "Costs must be different!"
    assert res_a.timeline.total_duration_months != res_b.timeline.total_duration_months, "Timelines must be different!"
    assert res_a.finance.monthly_emi != res_b.finance.monthly_emi, "EMIs must be different!"
    print("\n ALL ASSERTIONS PASSED: Projects A & B are completely dynamic and distinct!")


if __name__ == "__main__":
    run_verification()
