"""
End-to-End Live HTTP Test for BuildWise AI:
Creates Project A and Project B via REST API, triggers AI planning,
and verifies dynamic outputs across Blueprint, Floor Plan, House Layout,
Cost, Materials, Timeline, Risk, Interior, and Finance.
"""
import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"


def post_json(url, data):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_json(url):
    req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run():
    print("Connecting to live BuildWise AI Backend at:", BASE_URL)

    # 1. Create Project A
    print("\nCreating Project A: 40 Lakh | 2 BHK | 1 Floor | 30x40 Plot...")
    proj_a = post_json(f"{BASE_URL}/projects", {
        "project_name": "Project A - Compact Villa",
        "location": "Chennai (Porur)",
        "status": "planning"
    })
    id_a = proj_a["id"]
    print(f"Project A Created with ID: {id_a}")

    # Set requirements for Project A
    req_a = post_json(f"{BASE_URL}/projects/{id_a}/requirements", {
        "plot_width": 30.0,
        "plot_length": 40.0,
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

    # Generate/Retrieve AI Plan for Project A
    plan_a = get_json(f"{BASE_URL}/projects/{id_a}/ai-plan")
    print("Project A Plan successfully generated via LangGraph!")

    # 2. Create Project B
    print("\nCreating Project B: 60 Lakh | 4 BHK | 2 Floors | 40x60 Plot...")
    proj_b = post_json(f"{BASE_URL}/projects", {
        "project_name": "Project B - Luxury Duplex",
        "location": "Chennai (OMR)",
        "status": "planning"
    })
    id_b = proj_b["id"]
    print(f"Project B Created with ID: {id_b}")

    # Set requirements for Project B
    req_b = post_json(f"{BASE_URL}/projects/{id_b}/requirements", {
        "plot_width": 40.0,
        "plot_length": 60.0,
        "number_of_floors": 2,
        "bedrooms": 4,
        "bathrooms": 3,
        "parking_required": True,
        "budget": 6000000.0,
        "architectural_style": "Contemporary",
        "construction_type": "RCC Frame",
        "target_completion_months": 12,
        "sustainability_priority": "High",
        "special_requirements": "Rooftop solar and acoustic glazing"
    })

    # Generate/Retrieve AI Plan for Project B
    plan_b = get_json(f"{BASE_URL}/projects/{id_b}/ai-plan")
    print("Project B Plan successfully generated via LangGraph!")

    # 3. Dynamic Comparison
    print("\n" + "="*80)
    print("                PROJECT A vs PROJECT B: COMPARATIVE AUDIT")
    print("="*80)

    beds_a = [r["name"] for r in plan_a["design"]["rooms"] if "bedroom" in r["name"].lower()]
    beds_b = [r["name"] for r in plan_b["design"]["rooms"] if "bedroom" in r["name"].lower()]
    stairs_a = [r["name"] for r in plan_a["design"]["rooms"] if "staircase" in r["name"].lower()]
    stairs_b = [r["name"] for r in plan_b["design"]["rooms"] if "staircase" in r["name"].lower()]

    print(f"{'METRIC':<30} | {'PROJECT A (40L, 2 BHK, 1 Fl)':<25} | {'PROJECT B (60L, 4 BHK, 2 Fl)':<25}")
    print("-" * 86)
    print(f"{'Plot Size':<30} | {plan_a['design']['floor_plan']['plot_width']}x{plan_a['design']['floor_plan']['plot_length']} ft (1,200 sq.ft)   | {plan_b['design']['floor_plan']['plot_width']}x{plan_b['design']['floor_plan']['plot_length']} ft (2,400 sq.ft)")
    print(f"{'Total Built-Up Area':<30} | {plan_a['design']['total_built_up_area']:,.1f} sq.ft             | {plan_b['design']['total_built_up_area']:,.1f} sq.ft")
    print(f"{'Carpet Area':<30} | {plan_a['design']['carpet_area']:,.1f} sq.ft             | {plan_b['design']['carpet_area']:,.1f} sq.ft")
    print(f"{'Floors Count':<30} | {len(plan_a['design']['floor_plan']['floors'])} Level (G+0)             | {len(plan_b['design']['floor_plan']['floors'])} Levels (G+1)")
    print(f"{'Total Rooms Placed':<30} | {len(plan_a['design']['rooms'])} rooms                   | {len(plan_b['design']['rooms'])} rooms")
    print(f"{'Bedrooms Placed':<30} | {len(beds_a)} Beds ({', '.join(beds_a[:2])}) | {len(beds_b)} Beds (4 BHK across floors)")
    print(f"{'Staircase Structure':<30} | {len(stairs_a)} (Omitted for 1-Floor)  | {len(stairs_b)} (Core on both floors)")
    print(f"{'Turnkey Estimated Cost':<30} | INR {plan_a['cost']['total_estimated_cost']:,.0f}              | INR {plan_b['cost']['total_estimated_cost']:,.0f}")
    print(f"{'Unit Rate (INR/sq.ft)':<30} | INR {plan_a['cost']['cost_per_sqft']:,.0f}/sq.ft             | INR {plan_b['cost']['cost_per_sqft']:,.0f}/sq.ft")
    print(f"{'Budget Status':<30} | {plan_a['cost']['budget_comparison']['status']} (INR {abs(plan_a['cost']['budget_comparison']['variance']):,.0f} surplus) | {plan_b['cost']['budget_comparison']['status']} (INR {plan_b['cost']['budget_comparison']['variance']:,.0f} overrun)")
    print(f"{'Sustainability Rating':<30} | {plan_a['materials']['overall_sustainability_rating'][:23]} | {plan_b['materials']['overall_sustainability_rating'][:23]}")
    print(f"{'CPM Timeline Duration':<30} | {plan_a['timeline']['total_duration_months']:.1f} Months                | {plan_b['timeline']['total_duration_months']:.1f} Months")
    print(f"{'Overall Risk Level':<30} | {plan_a['risks']['overall_risk_level']} (Score {plan_a['risks']['average_risk_score']:.1f})          | {plan_b['risks']['overall_risk_level']} (Score {plan_b['risks']['average_risk_score']:.1f})")
    print(f"{'Interior Scheme Theme':<30} | {plan_a['interior']['style_theme'][:23]} | {plan_b['interior']['style_theme'][:23]}")
    print(f"{'Loan Principal Amount':<30} | INR {plan_a['finance']['loan_amount']:,.0f}              | INR {plan_b['finance']['loan_amount']:,.0f}")
    print(f"{'Monthly EMI':<30} | INR {plan_a['finance']['monthly_emi']:,.0f}/mo               | INR {plan_b['finance']['monthly_emi']:,.0f}/mo")

    # Assertions
    assert len(beds_a) == 2, f"Expected 2 bedrooms for A, got {len(beds_a)}"
    assert len(beds_b) == 4, f"Expected 4 bedrooms for B, got {len(beds_b)}"
    assert len(plan_a["design"]["floor_plan"]["floors"]) == 1, "Expected 1 floor for A"
    assert len(plan_b["design"]["floor_plan"]["floors"]) == 2, "Expected 2 floors for B"
    assert len(stairs_a) == 0, "Project A (1 floor) must have 0 staircases"
    assert len(stairs_b) == 2, "Project B (2 floors) must have 2 staircase representations"
    assert plan_a["cost"]["total_estimated_cost"] != plan_b["cost"]["total_estimated_cost"]
    assert plan_a["timeline"]["total_duration_months"] != plan_b["timeline"]["total_duration_months"]
    assert plan_a["finance"]["monthly_emi"] != plan_b["finance"]["monthly_emi"]

    print("\nSUCCESS: All live HTTP assertions passed! BuildWise AI is genuinely dynamic!")
    return id_a, id_b


if __name__ == "__main__":
    run()
