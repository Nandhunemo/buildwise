import sys
import json
import urllib.request

# Ensure UTF-8 output on Windows console
sys.stdout.reconfigure(encoding='utf-8')

base = "http://127.0.0.1:8000"

def post(path, d=None):
    if d is None:
        d = {}
    data_bytes = json.dumps(d).encode()
    req = urllib.request.Request(f"{base}{path}", data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get(path):
    req = urllib.request.Request(f"{base}{path}", method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def main():
    print("==================================================")
    print("      BUILDWISE AI — LIVE MODEL VERIFICATION      ")
    print("==================================================")

    # 1. Health Check
    health = get("/api/health")
    print("\n[API HEALTH]:", health)

    # 2. Load Chennai Demo Project
    demo = post("/api/demo/load-chennai")
    pid = demo["project_id"]
    print(f"\n[DEMO PROJECT CREATED]: Project ID #{pid}")
    print(f"Project Name: {demo['project_name']}")
    print(f"Estimated Cost: ₹{demo['estimated_cost']:,.0f}")
    print(f"Health Score: {demo['health_score']}/100")

    # 3. Fetch Full Project Detail
    proj = get(f"/api/projects/{pid}")
    print(f"\n[PROJECT DETAILS]: Location = {proj['location']}, Versions = {len(proj['versions'])}")
    print(f"Requirements: {proj['requirement']['bedrooms']} BHK | Plot: {proj['requirement']['plot_width']}x{proj['requirement']['plot_length']} ft | Budget: ₹{proj['requirement']['budget']:,.0f}")

    # 4. Fetch Health Score
    hs = get(f"/api/projects/{pid}/health-score")
    print(f"\n[HEALTH SCORE]: {hs['overall_score']}/100 ({hs['grade']} - {hs['rating']})")
    print(f"Breakdown: Budget={hs['budget_score']}, Schedule={hs['schedule_score']}, Risk={hs['risk_score']}")

    # 5. Simulate What-If (3 BHK to 4 BHK)
    whatif = post(f"/api/projects/{pid}/what-if", {"bedrooms": 4, "interest_rate": 8.75})
    print(f"\n[WHAT-IF SIMULATION: 3 BHK -> 4 BHK]:")
    print(f"• Before: Bedrooms={whatif['before_summary']['bedrooms']}, Cost=₹{whatif['before_summary']['total_estimated_cost']:,.0f}, EMI=₹{whatif['before_summary']['monthly_emi']:,.0f}/mo")
    print(f"• After:  Bedrooms={whatif['after_summary']['bedrooms']}, Cost=₹{whatif['after_summary']['total_estimated_cost']:,.0f}, EMI=₹{whatif['after_summary']['monthly_emi']:,.0f}/mo")
    print(f"• Affected Modules: {', '.join(whatif['affected_modules'])}")

    # 6. Budget Optimizer
    opt = post(f"/api/projects/{pid}/optimize")
    print(f"\n[BUDGET OPTIMIZER]:")
    print(f"Original: ₹{opt['original_cost']:,.0f} -> Optimized: ₹{opt['optimized_cost']:,.0f} (Savings: ₹{opt['total_savings']:,.0f} / {opt['percentage_savings']}%)")

    # 7. AI Decisions
    decisions = get(f"/api/projects/{pid}/decisions")
    print(f"\n[AI DECISION LOG] (Showing top 3 of {len(decisions)}):")
    for d in decisions[:3]:
        print(f"• [{d['agent']}] (Confidence: {int(d['confidence']*100)}%): {d['decision']}")

    # 8. Contractors
    contractors = get("/api/contractors")
    print(f"\n[REGIONAL CONTRACTORS (DEMO DATA)] ({len(contractors)} found):")
    for c in contractors[:2]:
        print(f"• {c['name']} | Rating: ⭐ {c['rating']} | Cost: {c['estimated_cost_range_sqft']} | Avail: {c['availability']}")

    print("\n==================================================")
    print(" ALL 8 AGENTS & INTELLIGENCE ENGINES OPERATIONAL! ")
    print("==================================================")

if __name__ == "__main__":
    main()
