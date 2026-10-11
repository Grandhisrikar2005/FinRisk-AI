
from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# FINRISK AI - FASTAPI BACKEND
# =========================================================

app = FastAPI(
    title="FinRisk AI",
    description=(
        "Explainable financial NLP risk analysis and "
        "simulated tactical portfolio rebalancing."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# 1. FINANCIAL RISK KNOWLEDGE BASE
# =========================================================

RISK_PHRASES = {
    "Liquidity Risk": [
        "cash shortage",
        "insufficient cash flow",
        "liquidity crisis",
        "unable to meet short term obligations",
        "working capital shortage",
        "cash reserves are declining",
    ],
    "Credit Risk": [
        "loan default",
        "missed debt payments",
        "credit rating downgrade",
        "unable to repay debt",
        "debt repayment problems",
        "borrower may default",
    ],
    "Market Risk": [
        "stock prices are falling",
        "market volatility increased",
        "equity market decline",
        "share prices dropped sharply",
        "market uncertainty",
        "asset prices are declining",
    ],
    "Operational Risk": [
        "business operations disrupted",
        "system failure",
        "cybersecurity breach",
        "fraud investigation",
        "supply chain disruption",
        "regulatory compliance failure",
    ],
    "Profitability Risk": [
        "profits declined",
        "operating losses increased",
        "revenue fell significantly",
        "profit margins are shrinking",
        "quarterly earnings missed expectations",
        "business reported a loss",
    ],
}

PHRASE_RECORDS = [
    (category, phrase)
    for category, phrases in RISK_PHRASES.items()
    for phrase in phrases
]

REFERENCE_PHRASES = [
    phrase for _, phrase in PHRASE_RECORDS
]

# Fit once when the backend starts.
vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    sublinear_tf=True,
)

REFERENCE_VECTORS = vectorizer.fit_transform(
    REFERENCE_PHRASES
)


# The most recent analysis is used by Module A.
latest_analysis = {
    "risk_level": "Moderate",
    "risk_score": 50,
    "signals": [],
    "sentiment": "Neutral",
}


# =========================================================
# 2. REQUEST MODELS
# =========================================================

class AnalyzeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=5,
        max_length=20000,
        description="Financial news or social media text",
    )


class CompareRequest(BaseModel):
    texts: List[str] = Field(
        ...,
        min_length=2,
        max_length=10,
    )


# =========================================================
# 3. RISK CLASSIFICATION
# =========================================================

def get_risk_level(score: int) -> str:
    """Convert a heuristic score into a risk band."""
    if score >= 70:
        return "High"
    if score >= 40:
        return "Moderate"
    return "Low"


# =========================================================
# 4. SENTIMENT ANALYSIS
# =========================================================

def classify_sentiment(text: str) -> dict:
    """
    Simple keyword-based sentiment analysis.
    This is a heuristic, not a trained sentiment model.
    """
    positive_terms = {
        "growth", "grew", "profit", "profits",
        "profitable", "strong", "stronger",
        "increase", "increased", "record",
        "positive", "recovery", "improved",
        "improvement", "surplus", "expansion",
        "beat expectations",
    }

    negative_terms = {
        "loss", "losses", "decline", "declined",
        "fall", "fell", "drop", "dropped",
        "weak", "weaker", "shortage", "default",
        "debt", "crisis", "fraud", "breach",
        "disruption", "downgrade",
        "missed expectations", "bankruptcy",
        "insolvency",
    }

    lower_text = text.lower()

    positive_hits = sorted(
        term for term in positive_terms
        if term in lower_text
    )

    negative_hits = sorted(
        term for term in negative_terms
        if term in lower_text
    )

    if len(positive_hits) > len(negative_hits):
        label = "Positive"
    elif len(negative_hits) > len(positive_hits):
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "label": label,
        "positive_terms": positive_hits,
        "negative_terms": negative_hits,
        "method": (
            "Keyword heuristic; not a trained sentiment model."
        ),
    }


# =========================================================
# 5. NLP RISK ENGINE
# =========================================================

def analyze_financial_text(text: str) -> dict:
    """
    Compare financial text against predefined risk phrases
    using TF-IDF vectors and cosine similarity.
    """
    text = text.strip()

    if len(text) < 5:
        raise HTTPException(
            status_code=422,
            detail="Please provide at least five characters.",
        )

    input_vector = vectorizer.transform([text])

    similarities = cosine_similarity(
        input_vector,
        REFERENCE_VECTORS,
    )[0]

    # Find the strongest phrase match in each category.
    best_matches = {}

    for index, similarity in enumerate(similarities):
        category, phrase = PHRASE_RECORDS[index]
        value = float(similarity)

        if (
            category not in best_matches
            or value > best_matches[category]["similarity"]
        ):
            best_matches[category] = {
                "category": category,
                "similarity": round(value, 4),
                "matched_phrase": phrase,
            }

    # Remove weak textual matches.
    signals = [
        match
        for match in best_matches.values()
        if match["similarity"] >= 0.12
    ]

    signals.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    # This is a heuristic score, not a probability.
    if signals:
        strongest = signals[0]["similarity"]

        second_strongest = (
            signals[1]["similarity"]
            if len(signals) > 1
            else 0.0
        )

        score = round(
            min(
                100,
                30
                + strongest * 65
                + second_strongest * 15,
            )
        )
    else:
        score = 15

    risk_level = get_risk_level(score)
    sentiment = classify_sentiment(text)

    if risk_level == "High":
        alert = (
            "HIGH RISK REVIEW: Strong textual risk matches "
            "were found. Verify the source and investigate."
        )
        action = (
            "Review liquidity, debt obligations, and original "
            "financial disclosures before taking action."
        )

    elif risk_level == "Moderate":
        alert = (
            "MODERATE RISK REVIEW: Some risk indicators may "
            "be present. Examine context and evidence."
        )
        action = (
            "Review matched phrases and compare them with "
            "reliable company disclosures."
        )

    else:
        alert = (
            "LOW MATCHED RISK: Few strong matches were found "
            "in the current phrase library."
        )
        action = (
            "Review other relevant financial information. "
            "A low score does not establish that a company "
            "is financially safe."
        )

    explanation = (
        "Financial text was compared with a predefined risk "
        "phrase library using TF-IDF cosine similarity. "
        "Similarity measures textual resemblance, not the "
        "probability of financial distress."
    )

    return {
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "risk_level": risk_level,
        "risk_score": score,
        "signals": signals,
        "sentiment": sentiment,
        "alert": alert,
        "recommended_action": action,
        "explanation": explanation,
        "disclaimer": (
            "Experimental educational prototype. Scores are "
            "heuristic, not calibrated probabilities or "
            "validated financial predictions. Not financial advice."
        ),
    }


# =========================================================
# 6. MODULE A: PORTFOLIO REBALANCING
# =========================================================

def calculate_portfolio(
    risk_level: str,
    risk_score: int,
) -> dict:
    """
    Generate illustrative portfolio allocations.
    These rules are educational heuristics only.
    """

    baseline = {
        "Equity": 40.0,
        "Bonds": 35.0,
        "Gold": 15.0,
        "Cash": 10.0,
    }

    profiles = {
        "High": {
            "Equity": 20.0,
            "Bonds": 40.0,
            "Gold": 20.0,
            "Cash": 20.0,
        },
        "Moderate": {
            "Equity": 40.0,
            "Bonds": 35.0,
            "Gold": 15.0,
            "Cash": 10.0,
        },
        "Low": {
            "Equity": 60.0,
            "Bonds": 25.0,
            "Gold": 10.0,
            "Cash": 5.0,
        },
    }

    after = profiles[risk_level]

    allocations = [
        {
            "asset": asset,
            "before_weight": baseline[asset],
            "after_weight": after[asset],
            "change": round(
                after[asset] - baseline[asset],
                2,
            ),
        }
        for asset in baseline
    ]

    total_before = round(sum(baseline.values()), 2)
    total_after = round(sum(after.values()), 2)

    return {
        "portfolio_name": (
            "FinRisk AI Illustrative Tactical Portfolio"
        ),
        "status": "success",
        "risk_level": risk_level,
        "risk_score": risk_score,
        "before_weights": baseline,
        "weights": after,
        "allocations": allocations,
        "total_before": total_before,
        "total_after": total_after,
        "allocation_check_passed": (
            abs(total_after - 100.0) < 0.001
        ),
        "explanation": (
            f"The {risk_level.lower()}-risk heuristic selects "
            "an illustrative allocation. Higher detected risk "
            "shifts the simulation away from equity and toward "
            "bonds, gold, and cash."
        ),
        "disclaimer": (
            "Educational simulation only; not investment advice "
            "or a live portfolio."
        ),
    }


# =========================================================
# 7. API ROUTES
# =========================================================

@app.get("/")
def home():
    return {
        "project": "FinRisk AI",
        "status": "running",
        "version": "2.0.0",
        "endpoints": [
            "GET /",
            "GET /health",
            "POST /analyze",
            "GET /portfolio",
            "POST /compare",
            "GET /evaluation",
        ],
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    global latest_analysis

    result = analyze_financial_text(request.text)

    # Save this result for the portfolio module.
    latest_analysis = {
        "risk_level": result["risk_level"],
        "risk_score": result["risk_score"],
        "signals": result["signals"],
        "sentiment": result["sentiment"]["label"],
    }

    return result


@app.get("/portfolio")
def get_portfolio():
    return calculate_portfolio(
        latest_analysis["risk_level"],
        latest_analysis["risk_score"],
    )


@app.post("/compare")
def compare(request: CompareRequest):
    rows = []

    for index, text in enumerate(request.texts, start=1):
        result = analyze_financial_text(text)

        rows.append({
            "headline_number": index,
            "text": text,
            "risk_level": result["risk_level"],
            "risk_score": result["risk_score"],
            "sentiment": result["sentiment"]["label"],
            "top_signal": (
                result["signals"][0]["category"]
                if result["signals"]
                else "No strong match"
            ),
        })

    rows.sort(
        key=lambda item: item["risk_score"],
        reverse=True,
    )

    return {
        "results": rows,
        "note": (
            "Ranked by heuristic score; not a validated "
            "financial risk prediction."
        ),
    }


# =========================================================
# 8. SMALL EVALUATION / SMOKE-TEST SET
# =========================================================

EVALUATION_CASES = [
    (
        "The company faces a severe cash shortage and may "
        "default on its loan repayments.",
        "Liquidity Risk",
        "Liquidity and credit example",
    ),
    (
        "The borrower missed debt payments and the lender "
        "warned of a possible loan default.",
        "Credit Risk",
        "Credit risk example",
    ),
    (
        "Stock prices are falling sharply amid increased "
        "market volatility.",
        "Market Risk",
        "Market risk example",
    ),
    (
        "A cybersecurity breach disrupted business operations "
        "and triggered a fraud investigation.",
        "Operational Risk",
        "Operational risk example",
    ),
    (
        "Quarterly profits declined as revenue fell "
        "significantly and operating losses increased.",
        "Profitability Risk",
        "Profitability risk example",
    ),
    (
        "The company reported stronger quarterly revenue, "
        "rising profits, and a positive growth outlook.",
        "No strong risk match",
        "Positive control",
    ),
    (
        "The company announced a new office opening and an "
        "employee volunteering event.",
        "No strong risk match",
        "Unrelated-text control",
    ),
]


@app.get("/evaluation")
def evaluation():
    rows = []

    for text, expected, purpose in EVALUATION_CASES:
        result = analyze_financial_text(text)

        predicted = (
            result["signals"][0]["category"]
            if result["signals"]
            else "No strong risk match"
        )

        rows.append({
            "purpose": purpose,
            "expected_category": expected,
            "predicted_category": predicted,
            "top_match_correct": predicted == expected,
            "risk_level": result["risk_level"],
            "risk_score": result["risk_score"],
        })

    correct = sum(
        row["top_match_correct"]
        for row in rows
    )

    total = len(rows)

    return {
        "cases": rows,
        "correct_top_category_matches": correct,
        "total_cases": total,
        "observed_match_rate_percent": round(
            correct / total * 100,
            1,
        ),
        "note": (
            "This is a tiny hand-written smoke-test set, "
            "not a representative benchmark. Do not present "
            "its match rate as validated model accuracy."
        ),
    }
