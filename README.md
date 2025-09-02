# 📊 Indian Namkeen Market (INM) Intelligence Platform – Backend API (Dockerized)

This repository contains the backend for the **Indian Namkeen Market (INM) Intelligence Platform**, designed to analyze and serve insights across **205+ KPIs** related to Haldiram and other major Indian snack brands. It delivers strategic analytics covering market landscape, competitive benchmarking, brand perception, consumer behavior, and advanced OSINT indicators — all exposed through a clean FastAPI-based interface.

---

## 📦 Key Highlights

- ✅ 205+ structured KPIs across 9 strategic intelligence sections  
- ⚙️ FastAPI backend with modular design and clean routing  
- 📁 Excel-based data pipelines using Pandas  
- 📊 Chart and metric endpoints for analysis and dashboards  
- 🐳 Fully Dockerized for isolated and scalable deployment

---

## 🧠 KPI Intelligence Framework

| Section | Description | Count |
|--------|-------------|-------|
| A | **Market & Industry Landscape** – Market size, growth, trends, tech, investments | 15 KPIs |
| B | **Competitive Landscape** – Product range, pricing, platform reach, social presence | 25 KPIs |
| C | **Haldiram Brand Perception & Online Presence** – Ratings, reviews, SEO, social metrics | 30 KPIs |
| D | **Consumer Insights (Public Data)** – Gifting, unmet needs, loyalty, demographic cues | 15 KPIs |
| E | **SWOT-Specific Indicators** – Derived strengths, weaknesses, opportunities, threats | 15 KPIs |
| F | **Advanced Market & Category Dynamics** – Trend velocity, Q-commerce, cannibalization | 20 KPIs |
| G | **Advanced Competitive Intelligence** – Pivot tracking, influencer ROI, partnerships | 30 KPIs |
| H | **Advanced Haldiram Brand Performance** – Sentiment drivers, content success, product icons | 25 KPIs |
| I | **Consumer Behavior & Journey Insights (OSINT)** – Journey mapping, switching, purchase intent | 30 KPIs |

📄 **Methodology Source**: See `KPIs.pdf` for complete breakdown and data logic.

---

## 🗂️ Project Structure


inm_docker/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── routers/             # API route definitions
│   ├── services/            # KPI logic and data processing
│   ├── models/              # Pydantic schemas
│   └── utils/               # Helpers (loaders, filters)
├── data/                    # Excel/CSV data files
├── Dockerfile               # Docker image configuration
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation


## 📊 Example API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/kpis/brands/` | List of all tracked brands |
| `/kpis/category/Namkeen` | KPIs filtered for Namkeen category |
| `/charts/engagement/haldiram` | Engagement plot for Haldiram |
| `/compare/search-volume` | Search interest comparison across brands |
| `/swot/haldiram` | Derived SWOT metrics for Haldiram |

📍 Full API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 👤 Author

**Yashi Gupta** 📧 gupta1803yashi@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/yashi-gupta-101808)

---

## 📄 License

This repository is intended strictly for academic and research purposes.  
For external use, collaboration, or distribution, please contact the author.

---

## ▶️ Quick Start

```bash
docker build -t inm-backend .
docker run -d -p 8000:8000 inm-backend
Then open http://localhost:8000/docs to explore the API interactively.
