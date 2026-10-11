# 📊 FinRisk AI — Explainable Financial Risk Intelligence

FinRisk AI is an AI-powered financial risk analysis prototype that analyzes financial text, identifies potential risk signals, estimates sentiment, and demonstrates risk-aware portfolio allocation through an interactive dashboard.

The project combines a **FastAPI backend**, **TF-IDF-based text similarity**, and a **Streamlit dashboard** to make financial text analysis and portfolio simulations accessible through a web application.

<p align="center">
  <strong>Explainable Risk Analysis • Financial NLP • Portfolio Simulation</strong>
</p>

## 🚀 Live Demo

- **Live Dashboard:** [Open FinRisk AI](https://finrisk-ai-bysrikar.streamlit.app/)
- **GitHub Repository:** [FinRisk-AI](https://github.com/Grandhisrikar2005/FinRisk-AI)
- **Backend API:** [FinRisk AI API](https://finrisk-ai-api.onrender.com)
- **Interactive API Documentation:** [Explore API Docs](https://finrisk-ai-api.onrender.com/docs)
- **Backend Health Check:** [Check Backend Health](https://finrisk-ai-api.onrender.com/health)

## 🎯 Problem Statement

Financial news and company announcements frequently contain information about liquidity pressure, credit exposure, market uncertainty, operational incidents, and profitability challenges.

Manually identifying these signals across multiple headlines can be time-consuming. FinRisk AI demonstrates how text similarity techniques and rule-based indicators can help organize financial information into interpretable risk assessments.

## 💡 Proposed Solution

FinRisk AI accepts financial headlines, statements, or short text inputs and produces an experimental risk assessment. It also provides a portfolio allocation simulation and allows users to compare multiple financial headlines.

The application emphasizes **explainability and transparency** by showing detected risk categories, matched reference phrases, heuristic scores, and system limitations.

## ✨ Key Features

### 1. Financial News Risk Analysis
- Accepts custom financial text and predefined sample headlines.
- Identifies potential liquidity, credit, market, operational, and profitability risk signals.
- Generates a heuristic risk score from 0 to 100.
- Assigns a High, Moderate, or Low risk level.

### 2. Explainable Risk Evidence
- Displays detected risk categories.
- Shows matched reference phrases and text similarity values.
- Provides a chart of similarity scores across detected categories.
- Presents a recommended review action based on the backend analysis.

### 3. Sentiment Estimation
- Uses positive and negative keyword indicators.
- Displays an estimated sentiment label.
- Shows matched positive and negative terms to help users interpret the result.

### 4. Tactical Portfolio Rebalancing Simulation
- Compares baseline portfolio weights with simulated risk-aware allocations.
- Displays equity, bonds, gold, and cash allocations.
- Visualizes allocation changes in an interactive chart.
- Checks whether simulated allocation weights total 100%.

### 5. Multi-Headline Comparison
- Analyzes multiple financial headlines in one request.
- Compares heuristic risk scores and risk levels.
- Displays a chart to help users compare the results.

### 6. Evaluation and Smoke Tests
- Runs a small, manually created evaluation set.
- Displays category-matching results.
- Provides a basic check of prototype behavior.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| API Server | Uvicorn |
| Text Feature Extraction | TF-IDF |
| Text Similarity | Cosine Similarity |
| Machine Learning Utilities | Scikit-learn |
| Dashboard | Streamlit |
| Data Processing | Pandas |
| Data Visualization | Plotly |
| HTTP Communication | Requests |
| Data Validation | Pydantic |
| Backend Hosting | Render |
| Dashboard Hosting | Streamlit Community Cloud |
| Version Control | Git and GitHub |

## 🏗️ System Architecture

```text
                 User
                  |
                  v
       Streamlit Web Dashboard
                  |
          HTTPS API Requests
                  |
                  v
          FastAPI Backend
                  |
                  v
       Financial Text Processing
                  |
          +-------+-------+
          |       |       |
          v       v       v
       TF-IDF  Keyword   Reference
       Similarity Sentiment Phrases
          |       |       |
          +-------+-------+
                  |
                  v
        Heuristic Risk Scoring
                  |
          +-------+-------+
          |               |
          v               v
    Risk Assessment   Portfolio Simulation
          |               |
          +-------+-------+
                  |
                  v
      Dashboard Results and Charts
```

## ⚙️ How It Works

### Step 1: Financial Text Input
The user enters financial text or selects a predefined example from the dashboard.

### Step 2: Text Representation
The backend uses TF-IDF representations to compare the input with a predefined collection of risk-related phrases.

### Step 3: Risk Signal Detection
Cosine similarity identifies text that resembles reference phrases associated with different financial risk categories.

### Step 4: Heuristic Risk Scoring
The backend calculates an experimental score based on detected similarity signals and maps it to a risk level.

### Step 5: Sentiment Estimation
Positive and negative keyword matches are used to estimate the sentiment of the text.

### Step 6: Portfolio Simulation
The application demonstrates predefined portfolio allocation scenarios and compares baseline weights with simulated allocations.

### Step 7: Visualization
The Streamlit dashboard displays risk indicators, evidence, sentiment, comparison results, and allocation charts.

## 📈 Example Portfolio Allocation Scenarios

The prototype demonstrates these illustrative allocation rules:

| Asset | High Risk | Moderate Risk | Low Risk |
|---|---:|---:|---:|
| Equity | 20% | 40% | 60% |
| Bonds | 40% | 35% | 25% |
| Gold | 20% | 15% | 10% |
| Cash | 20% | 10% | 5% |
| **Total** | **100%** | **100%** | **100%** |

These scenarios demonstrate predefined allocation rules. They are not optimized using live market data or personalized investor information.

## 🔌 Backend API Endpoints

**Base URL:** https://finrisk-ai-api.onrender.com

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Basic API information |
| `/health` | GET | Backend health check |
| `/analyze` | POST | Analyze financial text |
| `/portfolio` | GET | Retrieve simulated portfolio allocation |
| `/compare` | POST | Compare multiple financial headlines |
| `/evaluation` | GET | Run the small evaluation test set |
| `/docs` | GET | Interactive API documentation |

Use the interactive API documentation to inspect request schemas and response formats.

## 💻 Run Locally

### Prerequisites
- Python 3.11 or a compatible Python version
- pip
- Git (optional, for cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/Grandhisrikar2005/FinRisk-AI.git
cd FinRisk-AI
```

Alternatively, open your existing project folder in PyCharm.

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the FastAPI Backend

Open a terminal in the project directory:

```bash
python -m uvicorn main:app --reload
```

The backend will normally be available at:

- API: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Keep the backend terminal running.

### 5. Start the Streamlit Dashboard

Open a second terminal in the same directory. Activate the virtual environment if necessary, then run:

```bash
python -m streamlit run dashboard.py
```

Open the local dashboard at:

http://localhost:8501

The current dashboard configuration uses the deployed Render API. For fully local development, change the API base URL in `dashboard.py` to `http://localhost:8000`.

## 📁 Project Structure

```text
FinRisk-AI/
├── main.py
├── dashboard.py
├── requirements.txt
└── README.md
```

Additional configuration files may be present. The `.venv` directory is a local Python environment and should not be committed to GitHub.

## 🧪 Evaluation

The evaluation module runs a small, manually created set of examples to check whether the system identifies expected risk categories.

The resulting category-match rate is an exploratory prototype metric. It does not establish generalization, calibrated risk probabilities, or real-world financial forecasting accuracy.

Meaningful validation would require a larger, independently labeled dataset, a clearly defined evaluation protocol, and appropriate classification metrics.

## ⚠️ Limitations

- Risk detection uses TF-IDF similarity against predefined reference phrases.
- Sentiment estimation is keyword-based and may miss context, negation, sarcasm, or financial nuance.
- Risk scores are heuristic indicators, not probabilities of financial loss.
- The system does not use live financial news feeds or real-time market data.
- Portfolio allocations are simulated using predefined rules.
- The evaluation dataset is small and manually created.
- Results have not been validated for real-world financial decision-making.

## 🔮 Future Enhancements

- Integrate financial news APIs and real-time market data.
- Explore financial-domain language models for risk classification and sentiment analysis.
- Train and validate models on labeled financial datasets.
- Add historical risk tracking, alerts, and trend analysis.
- Expand evaluation with independent test data and standard metrics.
- Add persistent storage and user authentication if needed.
- Improve deployment monitoring and automated tests.

## 🔒 Disclaimer

FinRisk AI is an educational and hackathon prototype. Its outputs are experimental and should not be used as the sole basis for investment, lending, or risk-management decisions.

The application does not provide guaranteed predictions or personalized financial advice. Portfolio allocations are illustrative simulations and are not recommendations to buy or sell financial assets.

## 👨‍💻 Author

**Grandhi Venkata Sai Srikar**

- GitHub: [Grandhisrikar2005](https://github.com/Grandhisrikar2005)
- LinkedIn: [Grandhi Venkata Sai Srikar](https://www.linkedin.com/in/grandhi-venkata-sai-srikar)

---

<p align="center">
  Built as an experimental financial NLP and risk-analysis project.
</p>
