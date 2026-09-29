# BuildWise AI — Intelligent Home Construction Planning Platform

**BuildWise AI** is an autonomous multi-agent intelligence platform for residential home construction planning. It transforms homeowner requirements into structured 2D architectural spatial plans, deterministic bills of quantities (Schedule of Rates), CPM construction schedules, risk matrices, interior design schemes, and bank loan amortization schedules.

---

## 🌟 Key Features Across All Phases

### 🤖 1. Specialized Modular AI Agents (Phase 2)
Coordinated via **LangGraph StateGraph** over a shared Pydantic `ProjectState`:
- **Requirement Agent**: NLP parameter extraction, building bye-law checks, and missing information detection.
- **Design Agent**: 2D spatial zoning, room dimensions, built-up vs carpet areas, and design rationale.
- **Cost Estimation Agent**: Deterministic Python Schedule of Rates (SOR) calculation with 7.5% contingency.
- **Material Recommendation Agent**: Eco-durability material rating (0-10) and green building standards.
- **Timeline Agent**: Precedence Diagramming Method (PDM) CPM scheduling with Critical Path tracking.
- **Risk Prediction Agent**: 8-category risk matrix calculation ($P \times I$ index) with actionable mitigations.
- **Interior Design Agent**: Room-wise ergonomic layouts, lighting plans, and color palette harmonies.
- **Finance Agent**: Deterministic home loan EMI amortization and milestone S-curve cash flow projections.

### 🧠 2. Advanced Intelligence & Feasibility (Phase 3)
- **Budget Optimizer**: Identifies major cost contributors and computes itemized alternatives with savings.
- **What-If Scenario Simulator**: Simulates variations in bedrooms, budget, floors, materials, and interest rates.
- **Conflict Detector**: Validates realistic engineering constraints and flags spatial/financial/schedule conflicts.
- **Project Health Score**: 0–100 weighted index evaluating budget, timeline, risk, design, and material feasibility.
- **AI Decision Audit Log**: Traceable log of automated choices with rationale, confidence, and timestamps.
- **ChromaDB RAG Knowledge Base**: Domain guidelines, IS 456 codes, and green building standards.
- **Machine Learning Risk Pipeline**: Random Forest and Gradient Boosting delay and cost-overrun classifiers.

### 💻 3. Frontend & Visualizations (Phase 4 & 5)
- **Executive Dashboard**: Real-time project KPIs, Health Score gauge, and agent execution monitors.
- **2D Floor Plan Canvas**: Visual room layout, zones, dimensions, and natural light indicators.
- **CPM Gantt Schedule**: Visual task timelines and critical path highlights.
- **5×5 Risk Matrix**: Visual heat map of risk probability vs severity.
- **Consolidated PDF Report Generator**: Instant 16-section project feasibility report download.
- **Verified Contractor Marketplace**: Regional contractor recommendations with ratings and cost ranges (DEMO DATA).

---

## 🎨 Theme & Design System

The UI follows the official presentation palette:
- **Primary**: `#224435` (Deep Construction Forest Green)
- **Secondary**: `#F9F4BE` (Warm Cream Accent)
- **Background**: `#FFFDE6` (Soft Ivory Canvas)
- **Dark**: `#233939` (Deep Slate Charcoal)
- **Light**: `#DDEEE6` (Pale Mint Container)

---

## 📁 Directory Structure

```
buildwise_project/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entrypoint, CORS, static frontend mount
│   │   ├── config.py                # Pydantic Settings & environment variable configuration
│   │   ├── api/
│   │   │   ├── __init__.py          # API router aggregator (/api prefix)
│   │   │   ├── health.py            # Service health check
│   │   │   ├── projects.py          # Project CRUD endpoints
│   │   │   ├── requirements.py      # Requirements CRUD endpoints
│   │   │   ├── ai_plan.py           # LangGraph AI Plan execution endpoint
│   │   │   ├── intelligence.py      # What-If, Budget Optimizer, Conflicts, Health Score
│   │   │   ├── ml_rag.py            # ML Delay/Overrun predictions and ChromaDB RAG search
│   │   │   └── report.py            # PDF report download, Contractor marketplace & Demo loader
│   │   ├── database/
│   │   │   ├── base.py              # DeclarativeBase
│   │   │   └── connection.py        # SQLAlchemy engine, session maker, get_db dependency
│   │   ├── models/
│   │   │   ├── project.py           # Project ORM model
│   │   │   ├── requirement.py       # Requirement ORM model
│   │   │   ├── project_version.py   # ProjectVersion ORM model
│   │   │   └── ai_plan.py           # AIPlan & AIDecision ORM models
│   │   ├── agents/
│   │   │   ├── base_agent.py        # BaseAgent with Gemini integration & fallback
│   │   │   ├── requirement_agent.py # Requirement extraction
│   │   │   ├── design_agent.py      # 2D spatial layout
│   │   │   ├── cost_agent.py        # Schedule of Rates & contingency
│   │   │   ├── material_agent.py    # Eco-durability recommendations
│   │   │   ├── timeline_agent.py    # CPM critical path
│   │   │   ├── risk_agent.py        # Risk matrix (P × I)
│   │   │   ├── interior_agent.py    # Room-wise interior styling
│   │   │   └── finance_agent.py     # Loan EMI & cash flow
│   │   ├── orchestration/
│   │   │   ├── state.py             # Shared ProjectState and AgentExecutionStatus
│   │   │   ├── graph.py             # LangGraph StateGraph pipeline
│   │   │   └── propagation.py       # Requirement dependency mapper
│   │   ├── intelligence/
│   │   │   ├── budget_optimizer.py  # Itemized budget reduction options
│   │   │   ├── what_if_simulator.py # Parameter delta simulation
│   │   │   ├── conflict_detector.py # Incompatible constraints detection
│   │   │   └── health_score.py      # 0-100 multidimensional health index
│   │   ├── rag/
│   │   │   ├── knowledge_base.py    # Curated construction guidelines
│   │   │   ├── ingestion.py         # ChromaDB indexing
│   │   │   └── retriever.py         # Semantic search retriever
│   │   ├── ml/
│   │   │   ├── preprocessing.py     # Labeled synthetic dataset generator
│   │   │   ├── training.py          # Random Forest & Gradient Boosting training
│   │   │   ├── predict.py           # Inference pipeline
│   │   │   └── evaluation.py        # Accuracy, F1, Confusion Matrix
│   │   └── services/
│   │       ├── project_service.py   # Project business logic
│   │       ├── contractor_service.py# Regional contractor recommendations
│   │       └── report_service.py    # ReportLab 16-section PDF report generator
│   ├── tests/                       # 44 automated test suites (100% pass rate)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html                   # HTML5 SPA entrypoint
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx                  # Main React dashboard & 15 sub-pages
│       ├── index.css                # Custom CSS design system
│       └── services/
│           └── api.js               # Centralized backend API client
└── README.md
```

---

## 🚀 Setup & Execution Guide

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Environment Configuration
Create or inspect `backend/.env`:
```env
DATABASE_URL=sqlite:///./buildwise.db
GEMINI_API_KEY=
LLM_PROVIDER=gemini
APP_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```
*(Note: If `GEMINI_API_KEY` is omitted, the system runs seamlessly in **Deterministic Demo Mode**).*

### 3. Run Application
From the `backend/` directory:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- **Web Dashboard & UI**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Service Health Check**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

*(Optional: If running Vite dev server: `cd frontend && npm run dev` on port 5173).*

---

## 🧪 Running Automated Tests

Run the full pytest suite covering all 44 unit, integration, and API tests:
```bash
python -m pytest backend/tests -v
```

---

## 📡 Core API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/health` | `GET` | Service status check |
| `/api/projects` | `POST` / `GET` | Create and list projects |
| `/api/projects/{id}` | `GET` / `PUT` / `DELETE` | Project detail, update & delete |
| `/api/projects/{id}/requirements` | `POST` / `GET` / `PUT` | Manage homeowner construction requirements |
| `/api/projects/{id}/ai-plan` | `POST` | Execute full 8-agent LangGraph workflow |
| `/api/projects/{id}/optimize` | `POST` | Generate budget optimization alternatives |
| `/api/projects/{id}/what-if` | `POST` | Recalculate affected modules for scenario changes |
| `/api/projects/{id}/conflicts` | `POST` | Detect unrealistic or incompatible combinations |
| `/api/projects/{id}/health-score` | `GET` | Calculate 0–100 Project Health Score |
| `/api/projects/{id}/decisions` | `GET` | Retrieve AI Decision Audit Log |
| `/api/projects/{id}/versions` | `GET` | List project snapshot versions |
| `/api/projects/{id}/versions/compare` | `GET` | Compare two project versions |
| `/api/projects/{id}/report` | `GET` | Download 16-section Consolidated PDF Report |
| `/api/contractors` | `GET` | Verified regional contractor recommendations |
| `/api/demo/load-chennai` | `POST` | One-click setup & AI planning for Chennai Demo Project |
| `/api/ml/predict` | `POST` | ML Delay and Cost-Overrun probability inference |
| `/api/rag/query` | `POST` | Search ChromaDB Construction Knowledge Base |

---

## 🏆 Chennai Demo Project Specifications

- **Location**: Chennai (Anna Nagar / OMR)
- **Plot Dimensions**: 30 × 50 ft (1,500 sq.ft)
- **Floors**: 2 Floors (G+1)
- **Bedrooms / Bathrooms**: 3 BHK / 3 Baths
- **Parking**: 1 Covered Parking Porch
- **Budget**: ₹50,00,000 (₹50 Lakh)
- **Style**: Modern Minimalist (RCC Frame Structure)
- **Target Timeline**: 10 Months
- **Health Score**: 92/100 (Grade A)
- **Turnkey Cost**: ₹48,50,000 (Within budget with ₹1.5L contingency buffer)
