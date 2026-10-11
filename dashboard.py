
import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# =========================================================
# FINRISK AI - STREAMLIT DASHBOARD
# =========================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="FinRisk AI | Risk Intelligence",
    page_icon="📊",
    layout="wide",
)

st.title("📊 FinRisk AI")
st.caption(
    "Explainable Financial NLP Risk Intelligence "
    "& Simulated Tactical Rebalancing"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.header("Risk Engine")
    st.write(f"Backend API: {API_URL}")

    st.info(
        "Analyze financial news, inspect matched evidence, "
        "compare headlines, and explore simulated allocations."
    )

    if st.button("Check backend health"):
        try:
            response = requests.get(
                f"{API_URL}/health",
                timeout=5,
            )
            response.raise_for_status()
            st.success("Backend is healthy.")
        except requests.RequestException:
            st.error(
                "Backend is not reachable. Start the FastAPI "
                "server in another terminal."
            )


# =========================================================
# SAMPLE FINANCIAL NEWS
# =========================================================

EXAMPLES = {
    "Liquidity and credit warning": (
        "The company faces a severe cash shortage and may "
        "default on its loan repayments."
    ),
    "Positive earnings": (
        "The company reports stronger quarterly revenue, "
        "rising profits, and an improved growth outlook."
    ),
    "Market disruption": (
        "Geopolitical tensions threaten global supply chains "
        "and increase market uncertainty as stock prices fall."
    ),
    "Operational incident": (
        "A cybersecurity breach disrupted business operations "
        "and triggered a fraud investigation."
    ),
    "Profitability pressure": (
        "Quarterly earnings missed expectations as revenue "
        "fell significantly and operating losses increased."
    ),
}


# =========================================================
# 1. FINANCIAL NEWS ANALYSIS
# =========================================================

st.subheader("1. Financial News Analysis")

selected = st.selectbox(
    "Choose a sample or enter custom text",
    ["Custom text"] + list(EXAMPLES.keys()),
)

news_text = st.text_area(
    "Financial news article or social media post",
    value=EXAMPLES.get(selected, ""),
    height=130,
    placeholder="Paste financial news here...",
)

if st.button("Analyze Financial Risk", type="primary"):
    if len(news_text.strip()) < 5:
        st.warning("Please enter at least five characters.")
    else:
        try:
            response = requests.post(
                f"{API_URL}/analyze",
                json={"text": news_text},
                timeout=30,
            )
            response.raise_for_status()

            st.session_state["last_result"] = response.json()
            st.session_state["last_text"] = news_text

        except requests.RequestException as exc:
            st.error(
                "Could not reach the API. Make sure main.py "
                "is running in the other terminal."
            )
            st.caption(str(exc))


# =========================================================
# 2. DISPLAY RISK ASSESSMENT
# =========================================================

result = st.session_state.get("last_result")

if result:
    st.divider()
    st.subheader("Risk Assessment")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Risk Level",
        result["risk_level"],
    )

    col2.metric(
        "Heuristic Score",
        f'{result["risk_score"]}/100',
    )

    col3.metric(
        "Detected Signals",
        len(result["signals"]),
    )

    sentiment = result.get("sentiment", {})

    col4.metric(
        "Text Sentiment",
        sentiment.get("label", "Unknown"),
    )

    # Visual alert based on the heuristic risk band.
    if result["risk_level"] == "High":
        st.error(result["alert"])
    elif result["risk_level"] == "Moderate":
        st.warning(result["alert"])
    else:
        st.success(result["alert"])

    st.markdown(
        "**Recommended review action:** "
        + result.get(
            "recommended_action",
            "Review the original source text.",
        )
    )

    st.write(result["explanation"])

    # -----------------------------------------------------
    # Risk evidence table and chart
    # -----------------------------------------------------

    signals = result.get("signals", [])

    if signals:
        signal_df = pd.DataFrame(signals)

        st.subheader("Explainable Risk Evidence")

        st.caption(
            "Similarity measures textual resemblance to the "
            "phrase library, not probability of financial distress."
        )

        display_df = signal_df.rename(
            columns={
                "category": "Risk category",
                "similarity": "Text similarity",
                "matched_phrase": "Closest reference phrase",
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        fig = px.bar(
            signal_df,
            x="category",
            y="similarity",
            color="category",
            hover_data=["matched_phrase"],
            title="Text Similarity by Risk Category",
            range_y=[0, 1],
            labels={
                "category": "Risk category",
                "similarity": "Cosine similarity",
            },
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:
        st.info(
            "No strong matches in the phrase library. "
            "This does not prove the text is risk-free."
        )

    # -----------------------------------------------------
    # Sentiment evidence and technical details
    # -----------------------------------------------------

    with st.expander("Sentiment evidence and limitations"):
        st.write(
            "Positive keyword matches:",
            ", ".join(
                sentiment.get("positive_terms", [])
            ) or "None",
        )

        st.write(
            "Negative keyword matches:",
            ", ".join(
                sentiment.get("negative_terms", [])
            ) or "None",
        )

        st.caption(
            sentiment.get("method", "")
        )

        st.caption(
            "Analysis timestamp: "
            + result.get("analyzed_at", "Unavailable")
        )

        st.caption(
            result.get("disclaimer", "")
        )


# =========================================================
# 3. MODULE A - TACTICAL INDEX REBALANCING
# =========================================================

st.divider()

st.subheader(
    "2. Module A — Tactical Index Rebalancing"
)

st.caption(
    "Illustrative rules only. Allocations are simulated, "
    "not live prices or investment recommendations."
)

try:
    response = requests.get(
        f"{API_URL}/portfolio",
        timeout=10,
    )
    response.raise_for_status()

    portfolio = response.json()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Portfolio Risk Level",
        portfolio["risk_level"],
    )

    col2.metric(
        "Risk Score",
        f'{portfolio["risk_score"]}/100',
    )

    col3.metric(
        "Total Allocation",
        f'{portfolio["total_after"]:.1f}%',
    )

    if portfolio["allocation_check_passed"]:
        st.success(
            "Allocation check passed: simulated weights total 100%."
        )
    else:
        st.error(
            "Allocation total is not 100%. Check the backend."
        )

    allocation_df = pd.DataFrame(
        portfolio["allocations"]
    )

    # Compare the baseline allocation with the simulated one.
    chart_df = allocation_df.melt(
        id_vars="asset",
        value_vars=[
            "before_weight",
            "after_weight",
        ],
        var_name="scenario",
        value_name="weight",
    )

    chart_df["scenario"] = chart_df["scenario"].map(
        {
            "before_weight": "Baseline",
            "after_weight": "Risk-adjusted simulation",
        }
    )

    fig = px.bar(
        chart_df,
        x="asset",
        y="weight",
        color="scenario",
        barmode="group",
        text="weight",
        title=(
            "Baseline vs Simulated Rebalanced Allocation"
        ),
        labels={
            "asset": "Asset",
            "weight": "Portfolio weight (%)",
            "scenario": "Scenario",
        },
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
    )

    fig.update_layout(
        yaxis_range=[0, 75],
        legend_title_text="",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # Display allocation changes in a table.
    st.subheader("Allocation Breakdown")

    allocation_display = allocation_df.rename(
        columns={
            "asset": "Asset",
            "before_weight": "Baseline weight (%)",
            "after_weight": "Simulated weight (%)",
            "change": "Change (percentage points)",
        }
    )

    st.dataframe(
        allocation_display,
        use_container_width=True,
        hide_index=True,
    )

    st.write(portfolio["explanation"])

    st.caption(
        portfolio["disclaimer"]
    )

except requests.RequestException as exc:
    st.error(
        "Portfolio unavailable. Make sure the FastAPI "
        "backend is running."
    )
    st.caption(str(exc))


# =========================================================
# 4. COMPARE MULTIPLE FINANCIAL HEADLINES
# =========================================================

st.divider()
st.subheader("3. Compare Multiple Headlines")

st.write(
    "Compare financial headlines and rank them using the "
    "experimental heuristic risk score."
)

default_headlines = [
    EXAMPLES["Liquidity and credit warning"],
    EXAMPLES["Positive earnings"],
    EXAMPLES["Market disruption"],
]

headline_inputs = []

for index, default_text in enumerate(
    default_headlines,
    start=1,
):
    headline_inputs.append(
        st.text_area(
            f"Headline {index}",
            value=default_text,
            height=75,
            key=f"compare_headline_{index}",
        )
    )

if st.button("Compare Headlines"):
    texts = [
        text.strip()
        for text in headline_inputs
        if len(text.strip()) >= 5
    ]

    if len(texts) < 2:
        st.warning(
            "Enter at least two headlines with five or more characters."
        )
    else:
        try:
            response = requests.post(
                f"{API_URL}/compare",
                json={"texts": texts},
                timeout=30,
            )
            response.raise_for_status()

            payload = response.json()
            comparison_df = pd.DataFrame(
                payload["results"]
            )

            st.subheader("Headline Comparison Results")

            st.dataframe(
                comparison_df,
                use_container_width=True,
                hide_index=True,
            )

            fig = px.bar(
                comparison_df,
                x="headline_number",
                y="risk_score",
                color="risk_level",
                hover_data=[
                    "text",
                    "sentiment",
                    "top_signal",
                ],
                title="Headline Risk Score Comparison",
                range_y=[0, 100],
                labels={
                    "headline_number": "Headline",
                    "risk_score": "Heuristic score",
                    "risk_level": "Risk level",
                },
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            st.caption(
                payload.get(
                    "note",
                    "Scores are experimental heuristics.",
                )
            )

        except requests.RequestException as exc:
            st.error(
                "Could not compare headlines. Check the backend."
            )
            st.caption(str(exc))


# =========================================================
# 5. EVALUATION / SMOKE TEST
# =========================================================

st.divider()
st.subheader("4. Evaluation and Smoke Tests")

st.caption(
    "Hand-written examples check basic behavior. "
    "They do not establish validated model accuracy."
)

if st.button("Run Evaluation Examples"):
    try:
        response = requests.get(
            f"{API_URL}/evaluation",
            timeout=30,
        )
        response.raise_for_status()

        evaluation = response.json()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Correct Top-Category Matches",
            evaluation["correct_top_category_matches"],
        )

        col2.metric(
            "Total Test Cases",
            evaluation["total_cases"],
        )

        col3.metric(
            "Observed Match Rate",
            f'{evaluation["observed_match_rate_percent"]:.1f}%',
        )

        evaluation_df = pd.DataFrame(
            evaluation["cases"]
        )

        st.dataframe(
            evaluation_df,
            use_container_width=True,
            hide_index=True,
        )

        st.info(evaluation["note"])

    except requests.RequestException as exc:
        st.error(
            "Could not load evaluation results. "
            "Check the backend."
        )
        st.caption(str(exc))


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "FinRisk AI is an experimental educational prototype. "
    "TF-IDF similarity and keyword sentiment are not validated "
    "financial predictions. Portfolio allocations are simulated "
    "and are not investment advice."
)
