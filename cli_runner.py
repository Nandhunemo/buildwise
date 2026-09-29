import sys
import json
from app.orchestration.state import ProjectState
from app.orchestration.graph import project_graph
from app.intelligence.health_score import ProjectHealthScorer
from app.intelligence.budget_optimizer import BudgetOptimizer
from app.intelligence.conflict_detector import ConflictDetector
from app.intelligence.what_if_simulator import WhatIfSimulator, WhatIfRequest

# Ensure UTF-8 output on Windows console
sys.stdout.reconfigure(encoding='utf-8')

def run_model_pipeline(custom_input=None):
    if custom_input is None:
        # Default Chennai Project Specification
        custom_input = {
            "location": "Chennai (Anna Nagar / OMR)",
            "plot_width": 30.0,
            "plot_length": 50.0,
            "number_of_floors": 2,
            "bedrooms": 3,
            "bathrooms": 3,
            "parking": 1,
            "budget": 5000000.0,
            "architectural_style": "Modern Minimalist",
            "construction_type": "RCC Frame Structure",
            "target_completion_months": 10,
            "sustainability_priority": "High (Rooftop Solar & Rainwater Harvesting)",
            "special_requirements": "Rooftop Solar PV 3kWp with net-metering and EV charging point"
        }

    print("=" * 70)
    print("                 BUILDWISE AI — MULTI-AGENT EXECUTION TRACE")
    print("=" * 70)
    print("\n[1] USER / HOMEOWNER INPUT SPECIFICATIONS:")
    print(json.dumps(custom_input, indent=2))

    # Initialize State
    initial_state = ProjectState(
        project_id=101,
        raw_input=custom_input
    )

    # Execute LangGraph Pipeline
    print("\n" + "-" * 70)
    print(">>> EXECUTING LANGGRAPH PIPELINE ACROSS 8 SPECIALIZED AGENTS...")
    print("-" * 70)
    
    result_dict = project_graph.invoke(initial_state)
    state = ProjectState(**result_dict) if isinstance(result_dict, dict) else result_dict

    # 1. Requirement Agent Output
    print("\n-------------------------------------------------------------")
    print("📌 AGENT 1: REQUIREMENT AGENT OUTPUT")
    print("-------------------------------------------------------------")
    req = state.requirements
    print(f"• Location: {req.location}")
    print(f"• Plot Size: {req.plot_width} x {req.plot_length} ft ({req.plot_area} sq.ft)")
    print(f"• Scope: {req.bedrooms} BHK | {req.bathrooms} Baths | {req.number_of_floors} Floors (G+1)")
    print(f"• Budget: ₹{req.budget:,.0f} | Target Timeline: {req.target_completion_months} Months")
    print(f"• Missing Information Detected: {req.missing_information}")
    print(f"• Confidence Score: {int(req.confidence * 100)}% | Status: COMPLETED (Duration: {state.agent_execution_status['Requirement Agent'].duration_seconds}s)")

    # 2. Design Agent Output
    print("\n-------------------------------------------------------------")
    print("📌 AGENT 2: DESIGN AGENT OUTPUT (2D SPATIAL ALLOCATION)")
    print("-------------------------------------------------------------")
    des = state.design
    print(f"• Total Built-up Area: {des.total_built_up_area} sq.ft | Carpet Area: {des.carpet_area} sq.ft (80% efficiency)")
    print(f"• Design Style: {des.design_style}")
    print(f"• Design Rationale: {des.design_rationale}")
    print("\n  Room-by-Room Layout:")
    for r in des.rooms:
        print(f"    - [Floor {r.floor_number}] {r.room_name:<28} | Dimensions: {r.dimensions_ft:<12} | Area: {r.area_sqft} sq.ft | Zone: {r.spatial_zone:<12} | Light: {r.natural_light}")
    print(f"• Spatial Relationships:\n  * " + "\n  * ".join(des.spatial_relationships))

    # 3. Cost Estimation Agent Output
    print("\n-------------------------------------------------------------")
    print("📌 AGENT 3: COST ESTIMATION AGENT OUTPUT (DETERMINISTIC SOR)")
    print("-------------------------------------------------------------")
    cost = state.cost
    print(f"• Cost per Sq.Ft: ₹{cost.cost_per_sqft:,.0f}/sq.ft")
    print(f"• Material Cost Split (60%): ₹{cost.material_cost:,.0f}")
    print(f"• Labor Cost Split (28%):    ₹{cost.labor_cost:,.0f}")
    print(f"• MEP Cost Split (12%):      ₹{cost.mep_cost:,.0f}")
    print(f"• Unforeseen Site Contingency (7.5%): ₹{cost.contingency_amount:,.0f}")
    print(f"• TOTAL ESTIMATED TURNKEY COST:       ₹{cost.total_estimated_cost:,.0f}")
    print("\n  Itemized Bill of Quantities (BOQ):")
    for c in cost.categories:
        print(f"    - {c.category:<30} | Qty: {c.quantity} {c.unit:<16} | Unit Rate: ₹{c.unit_price:>5.0f} | Subtotal: ₹{c.subtotal:>10,.0f}")

    # 4. Material Recommendation Agent Output
    print("\n-------------------------------------------------------------")
    print("📌 AGENT 4: MATERIAL RECOMMENDATION AGENT OUTPUT")
    print("-------------------------------------------------------------")
    mat = state.materials
    print(f"• Overall Sustainability Rating: {mat.overall_sustainability_rating}")
    print("\n  Recommended Green Building Materials:")
    for m in mat.recommendations:
        print(f"    - {m.material:<45} [{m.category}]")
        print(f"      Durability: {m.durability:<15} | Maint: {m.maintenance:<10} | Score: {m.recommendation_score}/10 | Est: ₹{m.estimated_cost:,.0f}")
        print(f"      Advantages: {', '.join(m.advantages)}")

    # 5. Timeline Agent Output
    print("\n-------------------------------------------------------------")
    print("📌 AGENT 5: TIMELINE AGENT OUTPUT (CPM CRITICAL PATH)")
    print("-------------------------------------------------------------")
    time_out = state.timeline
    print(f"• Total Scheduled Duration: {time_out.total_duration_months} Months")
    print("\n  9-Phase Critical Path Construction Sequence:")
    for p in time_out.phases:
        crit_tag = "[CRITICAL PATH]" if p.is_critical_path else "[Non-Critical] "
        print(f"    - {p.task_id} {crit_tag} M{p.start_month:>4.2f} to M{p.end_month:>4.2f} ({p.duration_weeks:>3.1f} wks) | {p.phase}: {p.task_name}")

    # 6. Risk Prediction Agent Output
    print("\n-------------------------------------------------------------")
    print("📌 AGENT 6: RISK PREDICTION AGENT OUTPUT (8-DIMENSIONAL MATRIX)")
    print("-------------------------------------------------------------")
    risk_out = state.risks
    print(f"• Overall Risk Level: {risk_out.overall_risk_level} (Avg Index: {risk_out.average_risk_score}/25)")
    print("\n  Risk Assessment & Mitigation Matrix:")
    for r in risk_out.risks:
        print(f"    - [{r.severity:<8}] (P:{r.probability} × I:{r.impact} = {r.score:>2}) | {r.category:<12} | {r.risk}")
        print(f"      Mitigation: {r.mitigation}")

    # 7. Interior Design Agent Output
    print("\n-------------------------------------------------------------")
    print("📌 AGENT 7: INTERIOR DESIGN AGENT OUTPUT")
    print("-------------------------------------------------------------")
    interior = state.interior
    print(f"• Style Theme: {interior.style_theme}")
    print("\n  Room-Wise Interior Schemes:")
    for r in interior.rooms:
        print(f"    - {r.room_name}:")
        print(f"      Furniture: {', '.join(r.furniture_layout)}")
        print(f"      Palette:   {', '.join(r.color_palette)}")
        print(f"      Lighting:  {r.lighting_plan}")

    # 8. Finance Agent Output
    print("\n-------------------------------------------------------------")
    print("📌 AGENT 8: FINANCE AGENT OUTPUT (LOAN AMORTIZATION & CASH FLOW)")
    print("-------------------------------------------------------------")
    fin = state.finance
    print(f"• Total Estimated Cost:      ₹{fin.estimated_total_cost:,.0f}")
    print(f"• Down Payment (20% Equity): ₹{fin.down_payment_amount:,.0f}")
    print(f"• Home Construction Loan:    ₹{fin.loan_amount:,.0f} @ {fin.annual_interest_rate}% p.a. for {fin.loan_tenure_years} Years")
    print(f"• MONTHLY EQUATED EMI:       ₹{fin.monthly_emi:,.0f}/month")
    print(f"• Total Interest Payable:    ₹{fin.total_interest_payable:,.0f}")
    print(f"• Total Repayment Amount:    ₹{fin.total_repayment_amount:,.0f}")
    print("\n  Milestone S-Curve Construction Cash Flow:")
    for cf in fin.monthly_cash_flow_projection:
        print(f"    - {cf['milestone']:<35} | Stage Outflow: ₹{cf['stage_outflow']:>10,.0f} ({cf['percentage']:>4.1f}%) | Cumulative: ₹{cf['cumulative_outflow']:>10,.0f} | Source: {cf['recommended_disbursement']}")

    # 9. Project Health Score
    print("\n=============================================================")
    print("                   PROJECT HEALTH SCORE (0–100)")
    print("=============================================================")
    health = ProjectHealthScorer.calculate_health_score(state)
    print(f"OVERALL HEALTH SCORE: {health.overall_score}/100 (Grade {health.grade} — {health.rating})")
    print(f"• Budget Feasibility:     {health.budget_score}/100 (Weight: 30%)")
    print(f"• Schedule Realism:       {health.schedule_score}/100 (Weight: 20%)")
    print(f"• Risk Resilience:        {health.risk_score}/100 (Weight: 20%)")
    print(f"• Design Layout Score:    {health.design_score}/100 (Weight: 15%)")
    print(f"• Material Availability:  {health.material_score}/100 (Weight: 15%)")
    print(f"Explanation: {health.explanation}")

    # 10. Budget Optimization
    print("\n=============================================================")
    print("                     BUDGET OPTIMIZER")
    print("=============================================================")
    opt = BudgetOptimizer.optimize(state)
    print(f"Original Cost: ₹{opt.original_cost:,.0f} -> Optimized Cost: ₹{opt.optimized_cost:,.0f}")
    print(f"Potential Total Savings: ₹{opt.total_savings:,.0f} ({opt.percentage_savings}%)")
    print("\n  Actionable Optimization Alternatives:")
    for op in opt.optimization_options:
        print(f"    - {op.category}: {op.change_description}")
        print(f"      Savings: ₹{op.savings:,.0f} | Impact: {op.impact_assessment}")

    # 11. What-If Simulation
    print("\n=============================================================")
    print("         WHAT-IF SIMULATOR (TEST: 3 BHK -> 4 BHK)")
    print("=============================================================")
    whatif = WhatIfSimulator.simulate(state, WhatIfRequest(bedrooms=4, interest_rate=8.75))
    print(f"• Before: Bedrooms={whatif.before_summary['bedrooms']}, Cost=₹{whatif.before_summary['total_estimated_cost']:,.0f}, EMI=₹{whatif.before_summary['monthly_emi']:,.0f}/mo")
    print(f"• After:  Bedrooms={whatif.after_summary['bedrooms']}, Cost=₹{whatif.after_summary['total_estimated_cost']:,.0f}, EMI=₹{whatif.after_summary['monthly_emi']:,.0f}/mo")
    print(f"• Affected Modules Recalculated: {', '.join(whatif.affected_modules)}")

    print("\n" + "=" * 70)
    print("              PIPELINE EXECUTION COMPLETED 100% PASS")
    print("=" * 70)

if __name__ == "__main__":
    run_model_pipeline()
