import streamlit as st
import pandas as pd
import plotly.express as px

import os

# Load global FinSight AI styling
css_path = "assets/style.css"

if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

st.set_page_config(
    page_title="Executive Report",
    page_icon="📋",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/credit_risk_cleaned.csv")

df = load_data()

st.title("📋 Executive Credit Portfolio Report")

st.write(
    "Comprehensive portfolio summary for senior management."
)

st.markdown("---")

# ============================================================
# KPI CARDS
# ============================================================

customers = len(df)

loan_value = df["loan_amnt"].sum()

avg_income = df["person_income"].mean()

default_rate = df["loan_status"].mean()*100

interest = df["loan_int_rate"].mean()

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Customers",f"{customers:,}")

c2.metric("Portfolio Value",f"${loan_value:,.0f}")

c3.metric("Average Income",f"${avg_income:,.0f}")

c4.metric("Default Rate",f"{default_rate:.2f}%")

c5.metric("Average Interest",f"{interest:.2f}%")

st.markdown("---")

# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

left,right=st.columns(2)

with left:

    st.info(f"""

### Portfolio Overview

Customers

**{customers:,}**

Portfolio Value

**${loan_value:,.0f}**

Average Income

**${avg_income:,.0f}**

Average Loan

**${df['loan_amnt'].mean():,.0f}**

""")

with right:

    st.warning(f"""

### Risk Overview

Default Rate

**{default_rate:.2f}%**

Average Interest

**{interest:.2f}%**

High Risk Customers

**{len(df[df['risk_label']=='High Risk']):,}**

Low Risk Customers

**{len(df[df['risk_label']=='Low Risk']):,}**

""")

st.markdown("---")
# ============================================================
# PORTFOLIO OVERVIEW
# ============================================================

st.header("📊 Portfolio Overview")

col1, col2 = st.columns(2)

# -----------------------------
# Loan Grade Distribution
# -----------------------------

grade_df = (
    df["loan_grade"]
    .value_counts()
    .reset_index()
)

grade_df.columns = ["Loan Grade", "Customers"]

fig1 = px.bar(
    grade_df,
    x="Loan Grade",
    y="Customers",
    color="Loan Grade",
    text="Customers",
    title="Loan Grade Distribution"
)

fig1.update_layout(
    template="plotly_white",
    showlegend=False
)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Risk Distribution
# -----------------------------

risk_df = (
    df["risk_label"]
    .value_counts()
    .reset_index()
)

risk_df.columns = ["Risk", "Customers"]

fig2 = px.pie(
    risk_df,
    names="Risk",
    values="Customers",
    hole=0.45,
    title="Portfolio Risk Distribution"
)

fig2.update_layout(template="plotly_white")

with col2:
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ============================================================
# CUSTOMER & LOAN OVERVIEW
# ============================================================

col3, col4 = st.columns(2)

loan_df = (
    df["loan_intent"]
    .value_counts()
    .reset_index()
)

loan_df.columns = ["Loan Purpose", "Customers"]

fig3 = px.bar(
    loan_df,
    x="Loan Purpose",
    y="Customers",
    color="Loan Purpose",
    text="Customers",
    title="Loan Purpose Distribution"
)

fig3.update_layout(
    template="plotly_white",
    showlegend=False,
    xaxis_tickangle=-20
)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

income_df = (
    df["income_category"]
    .value_counts()
    .reset_index()
)

income_df.columns = ["Income Category", "Customers"]

fig4 = px.bar(
    income_df,
    x="Income Category",
    y="Customers",
    color="Income Category",
    text="Customers",
    title="Customer Income Segments"
)

fig4.update_layout(
    template="plotly_white",
    showlegend=False
)

with col4:
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.header("🧠 Executive Insights")

most_grade = df["loan_grade"].mode()[0]
most_loan = df["loan_intent"].mode()[0]
most_income = df["income_category"].mode()[0]
most_home = df["person_home_ownership"].mode()[0]

insights = []

insights.append(
    f"The lending portfolio currently consists of {customers:,} customers."
)

insights.append(
    f"The largest lending segment is '{most_loan}'."
)

insights.append(
    f"Most approved loans belong to Grade '{most_grade}'."
)

insights.append(
    f"The dominant customer income segment is '{most_income}'."
)

insights.append(
    f"Most customers have '{most_home}' home ownership."
)

for i, insight in enumerate(insights, start=1):
    st.success(f"{i}. {insight}")

st.markdown("---")

# ============================================================
# RISK ASSESSMENT
# ============================================================

st.header("🚨 Portfolio Risk Assessment")

if default_rate < 10:
    st.success("🟢 Overall portfolio risk is LOW.")

elif default_rate < 20:
    st.warning("🟡 Portfolio risk is MODERATE.")

else:
    st.error("🔴 Portfolio risk is HIGH.")

risk_score = max(0, 100 - (default_rate * 2))

st.metric(
    "Overall Portfolio Health Score",
    f"{risk_score:.0f}/100"
)

st.progress(risk_score / 100)

st.markdown("---")

# ============================================================
# STRATEGIC RECOMMENDATIONS
# ============================================================

st.header("💡 Strategic Recommendations")

recommendations = []

if default_rate > 20:
    recommendations.append(
        "Increase income eligibility criteria to reduce portfolio risk."
    )

if interest > 12:
    recommendations.append(
        "Review high-interest lending strategies to improve repayment."
    )

recommendations.append(
    "Monitor high-risk customers using predictive analytics."
)

recommendations.append(
    "Use the Policy Simulator before implementing new lending policies."
)

recommendations.append(
    "Continuously track loan grade performance and default trends."
)

recommendations.append(
    "Prioritize low-risk customer segments for sustainable portfolio growth."
)

for rec in recommendations:
    st.info("✔ " + rec)

st.markdown("---")

# ============================================================
# FINAL MANAGEMENT DECISION
# ============================================================

st.header("🏛 Executive Decision")

if risk_score >= 80:

    decision = """
### ✅ Recommendation

The lending portfolio is healthy.

Current approval policies can be maintained while continuously monitoring
customer behaviour and loan performance.
"""

elif risk_score >= 60:

    decision = """
### 🟡 Recommendation

The portfolio is moderately healthy.

Minor adjustments to lending criteria are recommended to improve
portfolio quality while maintaining business growth.
"""

else:

    decision = """
### 🔴 Recommendation

The portfolio exhibits elevated risk.

Management should tighten lending policies,
increase borrower screening,
and reduce exposure to high-risk customer segments.
"""

st.success(decision)

st.markdown("---")

# ============================================================
# PROJECT CONCLUSION
# ============================================================

st.header("🎯 Project Conclusion")

st.write("""
**FinSight AI** is an Executive Financial Risk Intelligence Platform designed to
support data-driven lending decisions.

Unlike traditional dashboards that only describe historical data,
this platform combines:

- 📊 Interactive Business Intelligence
- ⚠️ Credit Risk Analytics
- 👥 Customer Segmentation
- 🧪 Policy Simulation
- 📋 Executive Reporting

The Policy Simulator enables decision-makers to evaluate different lending
strategies before implementation, helping balance portfolio growth with
financial risk.

This transforms the application from a reporting dashboard into a practical
Decision Support System for financial institutions.
""")

st.markdown("---")

st.caption(
    "Developed as an Information Visualization Project | FinSight AI | Business Analytics"
)