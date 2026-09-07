import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🏦",
    layout="wide"
)

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/credit_risk_cleaned.csv")
    return df

df = load_data()

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

st.sidebar.title("🏦 FinSight AI")

st.sidebar.markdown("## Executive Filters")

loan_purpose = st.sidebar.multiselect(
    "Loan Purpose",
    options=sorted(df["loan_intent"].unique()),
    default=sorted(df["loan_intent"].unique())
)

loan_grade = st.sidebar.multiselect(
    "Loan Grade",
    options=sorted(df["loan_grade"].unique()),
    default=sorted(df["loan_grade"].unique())
)

home = st.sidebar.multiselect(
    "Home Ownership",
    options=sorted(df["person_home_ownership"].unique()),
    default=sorted(df["person_home_ownership"].unique())
)

risk = st.sidebar.multiselect(
    "Risk Label",
    options=sorted(df["risk_label"].unique()),
    default=sorted(df["risk_label"].unique())
)

# -------------------------------------------------------
# FILTER DATA
# -------------------------------------------------------

filtered_df = df[
    (df["loan_intent"].isin(loan_purpose)) &
    (df["loan_grade"].isin(loan_grade)) &
    (df["person_home_ownership"].isin(home)) &
    (df["risk_label"].isin(risk))
]

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.title("🏦 Executive Financial Dashboard")

st.caption(
    "Interactive overview of customer portfolio, lending patterns and financial risk."
)

st.markdown("---")

# -------------------------------------------------------
# KPIs
# -------------------------------------------------------

total_customers = len(filtered_df)

total_loans = filtered_df["loan_amnt"].sum()

avg_income = filtered_df["person_income"].mean()

avg_interest = filtered_df["loan_int_rate"].mean()

default_rate = filtered_df["loan_status"].mean() * 100

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

c2.metric(
    "💰 Total Loan",
    f"${total_loans:,.0f}"
)

c3.metric(
    "📈 Avg Income",
    f"${avg_income:,.0f}"
)

c4.metric(
    "⚠ Default Rate",
    f"{default_rate:.2f}%"
)

c5.metric(
    "💵 Avg Interest",
    f"{avg_interest:.2f}%"
)

st.markdown("---")

# -------------------------------------------------------
# FIRST ROW
# -------------------------------------------------------

left, right = st.columns(2)

# Loan Purpose

loan_counts = (
    filtered_df["loan_intent"]
    .value_counts()
    .reset_index()
)

loan_counts.columns = ["Loan Purpose", "Customers"]

fig1 = px.bar(
    loan_counts,
    x="Loan Purpose",
    y="Customers",
    color="Loan Purpose",
    title="Loan Purpose Distribution",
    text="Customers"
)

fig1.update_layout(
    showlegend=False,
    template="plotly_white"
)

with left:
    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# Loan Grade

grade_counts = (
    filtered_df["loan_grade"]
    .value_counts()
    .reset_index()
)

grade_counts.columns = ["Grade", "Customers"]

fig2 = px.pie(
    grade_counts,
    names="Grade",
    values="Customers",
    title="Loan Grade Distribution",
    hole=0.45
)

fig2.update_layout(
    template="plotly_white"
)

with right:
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.markdown("---")
# =====================================================
# SECOND ROW
# =====================================================

col3, col4 = st.columns(2)

# -------------------------
# Home Ownership
# -------------------------

home_df = (
    filtered_df["person_home_ownership"]
    .value_counts()
    .reset_index()
)

home_df.columns = ["Home Ownership", "Customers"]

fig3 = px.pie(
    home_df,
    names="Home Ownership",
    values="Customers",
    title="Home Ownership Distribution"
)

fig3.update_layout(template="plotly_white")

with col3:
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# Age Group
# -------------------------

age_df = (
    filtered_df["age_group"]
    .value_counts()
    .reset_index()
)

age_df.columns = ["Age Group", "Customers"]

fig4 = px.bar(
    age_df,
    x="Age Group",
    y="Customers",
    color="Age Group",
    text="Customers",
    title="Customer Age Groups"
)

fig4.update_layout(
    showlegend=False,
    template="plotly_white"
)

with col4:
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# =====================================================
# THIRD ROW
# =====================================================

col5, col6 = st.columns(2)

# -------------------------
# Income Category
# -------------------------

income_df = (
    filtered_df["income_category"]
    .value_counts()
    .reset_index()
)

income_df.columns = ["Income Category", "Customers"]

fig5 = px.bar(
    income_df,
    x="Income Category",
    y="Customers",
    color="Income Category",
    text="Customers",
    title="Income Category Distribution"
)

fig5.update_layout(
    showlegend=False,
    template="plotly_white"
)

with col5:
    st.plotly_chart(fig5, use_container_width=True)

# -------------------------
# Risk Label
# -------------------------

risk_df = (
    filtered_df["risk_label"]
    .value_counts()
    .reset_index()
)

risk_df.columns = ["Risk Label", "Customers"]

fig6 = px.bar(
    risk_df,
    x="Risk Label",
    y="Customers",
    color="Risk Label",
    text="Customers",
    title="Risk Category"
)

fig6.update_layout(
    showlegend=False,
    template="plotly_white"
)

with col6:
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# =====================================================
# FOURTH ROW
# =====================================================

col7, col8 = st.columns(2)

# -------------------------
# Interest Category
# -------------------------

interest_df = (
    filtered_df["interest_category"]
    .value_counts()
    .reset_index()
)

interest_df.columns = ["Interest Category", "Customers"]

fig7 = px.pie(
    interest_df,
    names="Interest Category",
    values="Customers",
    hole=0.45,
    title="Interest Rate Categories"
)

fig7.update_layout(template="plotly_white")

with col7:
    st.plotly_chart(fig7, use_container_width=True)

# -------------------------
# Employment Category
# -------------------------

employment_df = (
    filtered_df["employment_category"]
    .value_counts()
    .reset_index()
)

employment_df.columns = ["Employment Category", "Customers"]

fig8 = px.bar(
    employment_df,
    x="Employment Category",
    y="Customers",
    color="Employment Category",
    text="Customers",
    title="Employment Category"
)

fig8.update_layout(
    showlegend=False,
    template="plotly_white"
)

with col8:
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

# =====================================================
# LOAN SIZE DISTRIBUTION
# =====================================================

loan_size_df = (
    filtered_df["loan_size"]
    .value_counts()
    .reset_index()
)

loan_size_df.columns = ["Loan Size", "Customers"]

fig9 = px.bar(
    loan_size_df,
    x="Loan Size",
    y="Customers",
    color="Loan Size",
    text="Customers",
    title="Loan Size Distribution"
)

fig9.update_layout(
    showlegend=False,
    template="plotly_white"
)

st.plotly_chart(fig9, use_container_width=True)

st.markdown("---")
# =====================================================
# EXECUTIVE DECISION SUPPORT
# =====================================================

st.markdown("## 🧠 Executive Decision Support")

# -------------------------
# Portfolio Health Score
# -------------------------

avg_income = filtered_df["person_income"].mean()
default_rate = filtered_df["loan_status"].mean() * 100
avg_interest = filtered_df["loan_int_rate"].mean()

score = 100

# Deduct for high defaults
score -= default_rate * 2

# Deduct for high interest
score -= avg_interest

# Reward higher customer income
score += avg_income / 5000

score = max(0, min(100, score))

if score >= 80:
    health = "🟢 Excellent"
elif score >= 60:
    health = "🟡 Good"
elif score >= 40:
    health = "🟠 Moderate Risk"
else:
    health = "🔴 High Risk"

st.metric(
    "Portfolio Health Score",
    f"{score:.0f}/100",
    health
)

st.markdown("---")

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.subheader("📊 Executive Insights")

most_purpose = filtered_df["loan_intent"].mode()[0]
most_grade = filtered_df["loan_grade"].mode()[0]
most_risk = filtered_df["risk_label"].mode()[0]
most_income = filtered_df["income_category"].mode()[0]

insight1, insight2 = st.columns(2)

with insight1:

    st.info(f"""
### Portfolio Summary

• Customers Analysed : **{len(filtered_df):,}**

• Most Common Loan Purpose : **{most_purpose}**

• Dominant Loan Grade : **{most_grade}**

• Average Customer Income : **${avg_income:,.0f}**

• Average Interest Rate : **{avg_interest:.2f}%**
""")

with insight2:

    st.warning(f"""
### Risk Summary

• Default Rate : **{default_rate:.2f}%**

• Dominant Risk Category : **{most_risk}**

• Largest Income Segment : **{most_income}**

• Portfolio Health : **{health}**
""")

st.markdown("---")

# =====================================================
# SMART RECOMMENDATIONS
# =====================================================

st.subheader("💡 Smart Recommendations")

recommendations = []

if default_rate > 20:
    recommendations.append(
        "Increase minimum income requirement to reduce default risk."
    )

if avg_interest > 15:
    recommendations.append(
        "Review lending strategy as customers are paying relatively high interest."
    )

if most_grade in ["E", "F", "G"]:
    recommendations.append(
        "Large proportion of lower-grade loans detected. Strengthen credit evaluation."
    )

if most_risk == "High Risk":
    recommendations.append(
        "Increase monitoring of high-risk customers and tighten approval criteria."
    )

if avg_income < 50000:
    recommendations.append(
        "Portfolio contains many lower-income applicants. Review affordability checks."
    )

if len(recommendations) == 0:
    recommendations.append(
        "Current portfolio appears stable. Continue monitoring key financial indicators."
    )

for i, rec in enumerate(recommendations, start=1):
    st.success(f"{i}. {rec}")

st.markdown("---")

# =====================================================
# RISK ALERTS
# =====================================================

st.subheader("🚨 Portfolio Alerts")

if default_rate >= 25:
    st.error("High default rate detected. Immediate review of lending policy recommended.")
elif default_rate >= 15:
    st.warning("Moderate default rate observed. Monitor customer segments closely.")
else:
    st.success("Portfolio default rate is currently within acceptable limits.")

if score >= 80:
    st.success("Portfolio Health Status: Excellent")
elif score >= 60:
    st.info("Portfolio Health Status: Good")
elif score >= 40:
    st.warning("Portfolio Health Status: Moderate")
else:
    st.error("Portfolio Health Status: Critical")

st.markdown("---")

# =====================================================
# ABOUT THIS DASHBOARD
# =====================================================

with st.expander("📖 About this Dashboard"):

    st.write("""
This Executive Dashboard is one module of the **FinSight AI – Executive Decision Support System for Credit Risk Management**.

The dashboard enables decision makers to:

- Monitor customer portfolios
- Analyse lending patterns
- Evaluate credit risk
- Understand customer demographics
- Support lending decisions through interactive visualisations

Unlike traditional dashboards that only display historical data, this platform is designed to support business decisions and will be extended with a Loan Approval Policy Simulator.
""")