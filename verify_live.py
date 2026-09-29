import json
import urllib.request

def request(url, method="GET", data=None):
    body = json.dumps(data).encode() if data is not None else None
    headers = {"Content-Type": "application/json"} if data is not None else {}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode())

def run_verification():
    base = "http://127.0.0.1:8000"
    
    # 1. Health
    status, health = request(f"{base}/api/health")
    print(f"Health [{status}]:", health)
    assert health["status"] == "healthy"

    # 2. Create Project
    status, proj = request(f"{base}/api/projects", method="POST", data={
        "project_name": "Skyline Heights",
        "location": "San Francisco, CA"
    })
    print(f"Created Project [{status}]:", proj)
    project_id = proj["id"]

    # 3. Create Requirements
    status, req = request(f"{base}/api/projects/{project_id}/requirements", method="POST", data={
        "plot_width": 45.0,
        "plot_length": 75.0,
        "number_of_floors": 2,
        "bedrooms": 4,
        "bathrooms": 3,
        "parking_required": True,
        "budget": 650000.0,
        "architectural_style": "Contemporary Minimalist",
        "construction_type": "Reinforced Concrete",
        "target_completion_months": 15,
        "sustainability_priority": "High",
        "special_requirements": "Rainwater harvesting & rooftop solar array"
    })
    print(f"Created Requirement [{status}]:", req)
    assert req["plot_area"] == 3375.0  # 45 * 75

    # 4. Get Project Details
    status, detail = request(f"{base}/api/projects/{project_id}")
    print(f"Project Details [{status}]: Versions count={len(detail['versions'])}, Has Requirement={detail['requirement'] is not None}")
    
    # 5. Update Project
    status, updated_proj = request(f"{base}/api/projects/{project_id}", method="PUT", data={"status": "in_progress"})
    print(f"Updated Project Status [{status}]: {updated_proj['status']}")

    print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_verification()
