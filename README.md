# FinRisk AI — AI-Powered Financial Risk Analysis

FinRisk AI is a prototype financial risk analysis dashboard that analyzes financial text, identifies potential risk signals, provides explainable results, and demonstrates risk-aware portfolio allocation.

The application combines a FastAPI backend with an interactive Streamlit dashboard to help users explore financial risk indicators through a simple interface.

## Key Features

- **Financial Risk Analysis:** Identifies potential liquidity, credit, market, operational, and profitability risks in financial text.
- **Explainable Results:** Displays detected risk categories and supporting evidence.
- **Risk Scoring:** Calculates a heuristic risk score from detected signals and assigns a High, Moderate, or Low risk level.
- **Sentiment Analysis:** Uses positive and negative keyword indicators to estimate the sentiment of financial text.
- **Portfolio Allocation Simulation:** Compares baseline portfolio weights with simulated risk-aware allocations.
- **Multi-Headline Comparison:** Analyzes and ranks multiple financial headlines.
- **Evaluation Module:** Runs a small, hand-written test set to examine category-matching performance.
- **Interactive Dashboard:** Presents risk metrics, evidence, sentiment, charts, and portfolio comparisons.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Backend API | FastAPI |
| API server | Uvicorn |
| Text analysis | Scikit-learn |
| Text similarity | TF-IDF and cosine similarity |
| Dashboard | Streamlit |
| Data handling | Pandas |
| Visualization | Plotly |
| HTTP requests | Requests |
| Data validation | Pydantic |

## System Architecture

```text
       User enters financial text
                  |
                  v
        Streamlit Dashboard
                  |
                  v
           FastAPI Backend
                  |
                  v
      Text Processing and Analysis
                  |
         +--------+---------+
         |        |         |
         v        v         v
       Risk    Sentiment   Evidence
     Detection  Analysis   Matching
         |        |         |
         +--------+---------+
                  |
                  v
       Risk Score and Risk Level
                  |
                  v
      Portfolio Allocation Simulation
                  |
                  v
       Results, Charts and Insights
```

## Project Structure

```text
FinRisk-AI/
├── main.py
├── dashboard.py
├── requirements.txt
└── README.md
```

Other files and folders may be present depending on your local setup. Do not upload your virtual environment or temporary files.

## Installation and Setup

### Prerequisites

- Python 3.11 or a compatible Python version
- pip
- Git (for version control and GitHub upload)

### 1. Clone the repository

After uploading the project to GitHub, clone it using:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FinRisk-AI
```

Alternatively, open your existing project directly in PyCharm.

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the backend

Open a terminal in the project directory and run:

```bash
python -m uvicorn main:app --reload
```

The backend should be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Keep this terminal running.

### 5. Start the dashboard

Open a second terminal in the same project directory. Activate the virtual environment if necessary, then run:

```bash
python -m streamlit run dashboard.py
```

Open the local URL displayed in the terminal, usually:

http://localhost:8501

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Provides basic API information |
| `/health` | GET | Checks backend health |
| `/analyze` | POST | Analyzes financial text and returns risk indicators |
| `/portfolio` | GET | Returns simulated portfolio allocation information |
| `/compare` | POST | Compares multiple financial text inputs |
| `/evaluation` | GET | Runs the small evaluation test set |

Use the interactive API documentation at `/docs` to inspect the available request schemas and responses.

## How It Works

### 1. Financial Text Input

The user enters a financial headline, statement, or short description into the dashboard.

### 2. Risk Signal Detection

The backend uses TF-IDF text representations and cosine similarity to compare the input with predefined risk-related phrases. It identifies potential categories such as liquidity, credit, market, operational, and profitability risk.

### 3. Risk Scoring

The prototype calculates a heuristic score based on the strongest detected similarity signals and maps the score to a risk level.

### 4. Sentiment Estimation

Positive and negative keyword indicators are used to estimate sentiment.

### 5. Portfolio Simulation

The application demonstrates how a portfolio allocation might change according to a selected risk profile. It displays baseline and simulated allocations for equity, bonds, gold, and cash.

### 6. Visualization

The dashboard displays the analysis results, evidence, sentiment indicators, and allocation comparisons.

## Portfolio Allocation Simulation

The prototype demonstrates the following example allocations:

| Asset | High Risk | Moderate Risk | Low Risk |
|---|---:|---:|---:|
| Equity | 20% | 40% | 60% |
| Bonds | 40% | 35% | 25% |
| Gold | 20% | 15% | 10% |
| Cash | 20% | 10% | 5% |
| **Total** | **100%** | **100%** | **100%** |

These allocations are illustrative simulation rules, not personalized investment recommendations.

## Evaluation

The evaluation module uses a small, manually created test set to check whether the text-analysis system matches expected risk categories.

The reported category-match rate is a prototype evaluation metric. It should not be interpreted as proof of real-world financial forecasting accuracy or clinical-style predictive reliability.

## Current Limitations

- Risk detection relies on predefined phrases and TF-IDF similarity rather than a trained financial forecasting model.
- Sentiment analysis uses keyword-based heuristics rather than a dedicated, validated financial sentiment model.
- Risk scores are heuristic indicators, not calibrated probabilities of financial loss.
- Portfolio allocations are simulated and do not use live market data, current asset prices, or personalized investor information.
- The evaluation set is small and manually created; larger, independently labeled datasets are required for meaningful validation.

## Future Enhancements

- Integrate financial news APIs and real-time market data.
- Explore domain-specific financial language models.
- Train and evaluate risk-classification models on labeled financial datasets.
- Improve sentiment analysis using financial NLP techniques.
- Add historical risk tracking, alerts, and trend analysis.
- Evaluate the system using larger datasets and appropriate classification metrics.
- Add user authentication and persistent storage if required.

## Disclaimer

FinRisk AI is an educational and hackathon prototype. Its outputs are experimental and should not be used as the sole basis for financial, investment, lending, or risk-management decisions. The system does not provide guaranteed predictions or personalized financial advice.

## Author

**Grandhi Venkata Sai Srikar**

- GitHub: https://github.com/Grandhisrikar2005
- LinkedIn: https://www.linkedin.com/in/grandhi-venkata-sai-srikar
