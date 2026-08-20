import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Risk Analytics",
    page_icon="⚠️",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/credit_risk_cleaned.csv")

df = load_data()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("⚠️ Risk Analytics")

risk_filter = st.sidebar.multiselect(
    "Risk Label",
    sorted(df["risk_label"].unique()),
    default=sorted(df["risk_label"].unique())
)

grade_filter = st.sidebar.multiselect(
    "Loan Grade",
    sorted(df["loan_grade"].unique()),
    default=sorted(df["loan_grade"].unique())
)

interest_filter = st.sidebar.multiselect(
    "Interest Category",
    sorted(df["interest_category"].unique()),
    default=sorted(df["interest_category"].unique())
)

filtered_df = df[
    (df["risk_label"].isin(risk_filter)) &
    (df["loan_grade"].isin(grade_filter)) &
    (df["interest_category"].isin(interest_filter))
]

st.title("⚠️ Risk Analytics")

st.write(
    "Analyse loan quality, customer risk, defaults and portfolio health."
)

st.markdown("---")

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

default_rate = filtered_df["loan_status"].mean() * 100

avg_interest = filtered_df["loan_int_rate"].mean()

high_risk = len(
    filtered_df[
        filtered_df["risk_label"] == "High Risk"
    ]
)

avg_loan = filtered_df["loan_amnt"].mean()

customers = len(filtered_df)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Customers", f"{customers:,}")

c2.metric("Default Rate", f"{default_rate:.2f}%")

c3.metric("High Risk", f"{high_risk:,}")

c4.metric("Average Interest", f"{avg_interest:.2f}%")

c5.metric("Average Loan", f"${avg_loan:,.0f}")

st.markdown("---")

# -------------------------------------------------
# LOAN GRADE
# -------------------------------------------------

left, right = st.columns(2)

grade = (
    filtered_df["loan_grade"]
    .value_counts()
    .reset_index()
)

grade.columns = ["Loan Grade", "Customers"]

fig1 = px.bar(
    grade,
    x="Loan Grade",
    y="Customers",
    color="Loan Grade",
    text="Customers",
    title="Loan Grade Distribution"
)

fig1.update_layout(
    showlegend=False,
    template="plotly_white"
)

with left:
    st.plotly_chart(fig1, use_container_width=True)

risk = (
    filtered_df["risk_label"]
    .value_counts()
    .reset_index()
)

risk.columns = ["Risk", "Customers"]

fig2 = px.pie(
    risk,
    names="Risk",
    values="Customers",
    hole=0.45,
    title="Risk Distribution"
)

fig2.update_layout(template="plotly_white")

with right:
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
# ============================================================
# INTEREST & DEFAULT ANALYSIS
# ============================================================

st.subheader("📈 Interest & Default Analysis")

col1, col2 = st.columns(2)

# -----------------------------
# Interest Category
# -----------------------------

interest_df = (
    filtered_df["interest_category"]
    .value_counts()
    .reset_index()
)

interest_df.columns = ["Interest Category", "Customers"]

fig3 = px.bar(
    interest_df,
    x="Interest Category",
    y="Customers",
    color="Interest Category",
    text="Customers",
    title="Interest Category Distribution"
)

fig3.update_layout(
    template="plotly_white",
    showlegend=False
)

with col1:
    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Default vs Non Default
# -----------------------------

default_df = (
    filtered_df["loan_status"]
    .value_counts()
    .reset_index()
)

default_df.columns = ["Loan Status", "Customers"]

default_df["Loan Status"] = default_df["Loan Status"].replace({
    0: "Non Default",
    1: "Default"
})

fig4 = px.pie(
    default_df,
    names="Loan Status",
    values="Customers",
    hole=0.45,
    title="Default vs Non Default"
)

fig4.update_layout(template="plotly_white")

with col2:
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ============================================================
# LOAN GRADE VS LOAN AMOUNT
# ============================================================

st.subheader("💰 Loan Amount Analysis")

col3, col4 = st.columns(2)

loan_grade = (
    filtered_df.groupby("loan_grade")["loan_amnt"]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    loan_grade,
    x="loan_grade",
    y="loan_amnt",
    color="loan_grade",
    text_auto=".0f",
    title="Average Loan Amount by Grade"
)

fig5.update_layout(
    template="plotly_white",
    showlegend=False,
    xaxis_title="Loan Grade",
    yaxis_title="Average Loan Amount"
)

with col3:
    st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# Interest Rate by Risk
# -----------------------------

fig6 = px.box(
    filtered_df,
    x="risk_label",
    y="loan_int_rate",
    color="risk_label",
    title="Interest Rate by Risk Category"
)

fig6.update_layout(
    template="plotly_white",
    showlegend=False
)

with col4:
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# ============================================================
# HOME OWNERSHIP VS RISK
# ============================================================

st.subheader("🏠 Customer Risk Profile")

col5, col6 = st.columns(2)

home_risk = (
    filtered_df.groupby(
        ["person_home_ownership", "risk_label"]
    )
    .size()
    .reset_index(name="Customers")
)

fig7 = px.bar(
    home_risk,
    x="person_home_ownership",
    y="Customers",
    color="risk_label",
    barmode="group",
    title="Risk by Home Ownership"
)

fig7.update_layout(
    template="plotly_white",
    xaxis_title="Home Ownership"
)

with col5:
    st.plotly_chart(fig7, use_container_width=True)

# -----------------------------
# Loan Purpose vs Default
# -----------------------------

purpose = (
    filtered_df.groupby(
        ["loan_intent", "loan_status"]
    )
    .size()
    .reset_index(name="Customers")
)

purpose["loan_status"] = purpose["loan_status"].replace({
    0: "Non Default",
    1: "Default"
})

fig8 = px.bar(
    purpose,
    x="loan_intent",
    y="Customers",
    color="loan_status",
    barmode="group",
    title="Loan Purpose vs Default"
)

fig8.update_layout(
    template="plotly_white",
    xaxis_tickangle=-20
)

with col6:
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")
# ============================================================
# PORTFOLIO RISK SCORE
# ============================================================

st.header("🧠 Portfolio Risk Assessment")

default_rate = filtered_df["loan_status"].mean() * 100
avg_interest = filtered_df["loan_int_rate"].mean()
high_risk_pct = (
    len(filtered_df[filtered_df["risk_label"] == "High Risk"])
    / len(filtered_df) * 100
) if len(filtered_df) > 0 else 0

risk_score = 100

risk_score -= default_rate * 1.8
risk_score -= avg_interest
risk_score -= high_risk_pct * 0.5

risk_score = max(0, min(100, risk_score))

if risk_score >= 80:
    status = "🟢 Low Portfolio Risk"
elif risk_score >= 60:
    status = "🟡 Moderate Portfolio Risk"
elif risk_score >= 40:
    status = "🟠 High Portfolio Risk"
else:
    status = "🔴 Critical Portfolio Risk"

st.metric(
    "Portfolio Risk Score",
    f"{risk_score:.0f}/100",
    status
)

st.markdown("---")

# ============================================================
# EXECUTIVE RISK SUMMARY
# ============================================================

st.header("📊 Executive Risk Summary")

left, right = st.columns(2)

most_grade = filtered_df["loan_grade"].mode()[0]
most_risk = filtered_df["risk_label"].mode()[0]
most_interest = filtered_df["interest_category"].mode()[0]

with left:

    st.info(f"""
### Portfolio Overview

• Customers Analysed

**{len(filtered_df):,}**

• Default Rate

**{default_rate:.2f}%**

• Average Interest

**{avg_interest:.2f}%**

• Dominant Loan Grade

**{most_grade}**
""")

with right:

    st.warning(f"""
### Risk Overview

• High Risk Customers

**{high_risk_pct:.1f}%**

• Largest Risk Category

**{most_risk}**

• Interest Segment

**{most_interest}**

• Portfolio Status

**{status}**
""")

st.markdown("---")

# ============================================================
# SMART RISK RECOMMENDATIONS
# ============================================================

st.header("💡 Risk Recommendations")

recommendations = []

if default_rate > 20:
    recommendations.append(
        "Increase the minimum income threshold for new applicants."
    )

if avg_interest > 12:
    recommendations.append(
        "Review pricing strategy for high-interest loans."
    )

if high_risk_pct > 30:
    recommendations.append(
        "Reduce exposure to high-risk customer segments."
    )

if most_grade in ["E", "F", "G"]:
    recommendations.append(
        "Strengthen approval criteria for lower credit grades."
    )

recommendations.append(
    "Continuously monitor portfolio performance using the Policy Simulator."
)

for i, item in enumerate(recommendations, start=1):
    st.success(f"{i}. {item}")

st.markdown("---")

# ============================================================
# PORTFOLIO ALERTS
# ============================================================

st.header("🚨 Portfolio Alerts")

if default_rate >= 25:
    st.error("Critical Alert: Portfolio default rate is significantly above target.")

elif default_rate >= 15:
    st.warning("Warning: Default rate requires closer monitoring.")

else:
    st.success("Portfolio default rate is within the acceptable range.")

if high_risk_pct >= 40:
    st.error("Large proportion of high-risk customers detected.")

elif high_risk_pct >= 25:
    st.warning("Moderate concentration of high-risk customers.")

else:
    st.success("High-risk customer proportion is under control.")

st.markdown("---")

# ============================================================
# NEXT STEP
# ============================================================

st.info("""
### Decision Support

The insights shown above describe the current portfolio.

The next module (**Policy Simulator**) allows managers to change lending rules
(such as minimum income, accepted loan grades, or previous default policy)
and immediately observe how those decisions affect approvals and portfolio risk.
""")

st.markdown("---")

st.caption("""
Risk Analytics is one component of the FinSight AI Executive Decision Support System.
It provides portfolio risk monitoring and supports data-driven lending decisions.
""")