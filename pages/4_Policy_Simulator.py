import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Policy Simulator",
    page_icon="🧪",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/credit_risk_cleaned.csv")

df = load_data()

# ============================================================
# TITLE
# ============================================================

st.title("🧪 Loan Approval Policy Simulator")

st.markdown("""
Simulate different lending policies and instantly observe their impact on
customer approvals, portfolio value and financial risk.
""")

st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Policy Controls")

minimum_income = st.sidebar.slider(
    "Minimum Annual Income ($)",
    min_value=0,
    max_value=int(df["person_income"].max()),
    value=30000,
    step=5000
)

minimum_employment = st.sidebar.slider(
    "Minimum Employment Length (Years)",
    min_value=0,
    max_value=20,
    value=1
)

allow_previous_default = st.sidebar.checkbox(
    "Allow Previous Defaulters",
    value=True
)

accepted_grades = st.sidebar.multiselect(
    "Accepted Loan Grades",
    sorted(df["loan_grade"].unique()),
    default=sorted(df["loan_grade"].unique())
)

maximum_interest = st.sidebar.slider(
    "Maximum Interest Rate (%)",
    min_value=float(df["loan_int_rate"].min()),
    max_value=float(df["loan_int_rate"].max()),
    value=float(df["loan_int_rate"].max())
)

st.sidebar.markdown("---")

simulate = st.sidebar.button("🚀 Run Simulation")

# ============================================================
# APPLY POLICY
# ============================================================

policy_df = df.copy()

policy_df = policy_df[
    policy_df["person_income"] >= minimum_income
]

policy_df = policy_df[
    policy_df["person_emp_length"] >= minimum_employment
]

policy_df = policy_df[
    policy_df["loan_grade"].isin(accepted_grades)
]

policy_df = policy_df[
    policy_df["loan_int_rate"] <= maximum_interest
]

if not allow_previous_default:
    policy_df = policy_df[
        policy_df["cb_person_default_on_file"] == "N"
    ]

st.markdown("---")

# ============================================================
# KPI CARDS
# ============================================================

approved = len(policy_df)

approval_rate = approved / len(df) * 100

portfolio_value = policy_df["loan_amnt"].sum()

estimated_default = policy_df["loan_status"].mean() * 100

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Approved Customers",
    f"{approved:,}"
)

c2.metric(
    "Approval Rate",
    f"{approval_rate:.2f}%"
)

c3.metric(
    "Portfolio Value",
    f"${portfolio_value:,.0f}"
)

c4.metric(
    "Estimated Default Rate",
    f"{estimated_default:.2f}%"
)

st.markdown("---")
# ============================================================
# SIMULATION VISUALIZATIONS
# ============================================================

st.header("📊 Policy Impact Dashboard")

# ------------------------------------------------------------
# BEFORE VS AFTER
# ------------------------------------------------------------

before = len(df)
after = len(policy_df)

compare = pd.DataFrame({
    "Scenario": ["Original Portfolio", "Approved After Policy"],
    "Customers": [before, after]
})

fig1 = px.bar(
    compare,
    x="Scenario",
    y="Customers",
    color="Scenario",
    text="Customers",
    title="Customer Approval Impact"
)

fig1.update_layout(
    template="plotly_white",
    showlegend=False
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ============================================================
# SECOND ROW
# ============================================================

left, right = st.columns(2)

# ------------------------------------------------------------
# Loan Grade Distribution
# ------------------------------------------------------------

grade_df = (
    policy_df["loan_grade"]
    .value_counts()
    .reset_index()
)

grade_df.columns = ["Loan Grade", "Customers"]

fig2 = px.bar(
    grade_df,
    x="Loan Grade",
    y="Customers",
    color="Loan Grade",
    text="Customers",
    title="Approved Loan Grades"
)

fig2.update_layout(
    template="plotly_white",
    showlegend=False
)

with left:
    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------------
# Risk Label
# ------------------------------------------------------------

risk_df = (
    policy_df["risk_label"]
    .value_counts()
    .reset_index()
)

risk_df.columns = ["Risk", "Customers"]

fig3 = px.pie(
    risk_df,
    names="Risk",
    values="Customers",
    hole=0.45,
    title="Risk Distribution After Policy"
)

fig3.update_layout(template="plotly_white")

with right:
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ============================================================
# THIRD ROW
# ============================================================

left, right = st.columns(2)

# ------------------------------------------------------------
# Loan Purpose
# ------------------------------------------------------------

purpose_df = (
    policy_df["loan_intent"]
    .value_counts()
    .reset_index()
)

purpose_df.columns = ["Loan Purpose", "Customers"]

fig4 = px.bar(
    purpose_df,
    x="Loan Purpose",
    y="Customers",
    color="Loan Purpose",
    text="Customers",
    title="Approved Loan Purpose"
)

fig4.update_layout(
    template="plotly_white",
    showlegend=False,
    xaxis_tickangle=-20
)

with left:
    st.plotly_chart(fig4, use_container_width=True)

# ------------------------------------------------------------
# Income Category
# ------------------------------------------------------------

income_df = (
    policy_df["income_category"]
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
    title="Approved Income Segments"
)

fig5.update_layout(
    template="plotly_white",
    showlegend=False
)

with right:
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ============================================================
# HOME OWNERSHIP
# ============================================================

home_df = (
    policy_df["person_home_ownership"]
    .value_counts()
    .reset_index()
)

home_df.columns = ["Home Ownership", "Customers"]

fig6 = px.pie(
    home_df,
    names="Home Ownership",
    values="Customers",
    title="Home Ownership of Approved Customers"
)

fig6.update_layout(template="plotly_white")

st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
# ============================================================
# DECISION IMPACT ANALYSIS
# ============================================================

st.header("🧠 Decision Impact Analysis")

original_customers = len(df)
approved_customers = len(policy_df)

customers_rejected = original_customers - approved_customers

approval_rate = (approved_customers / original_customers) * 100

original_default = df["loan_status"].mean() * 100
new_default = policy_df["loan_status"].mean() * 100 if approved_customers > 0 else 0

risk_reduction = original_default - new_default

estimated_interest = (
    policy_df["loan_amnt"] * policy_df["loan_int_rate"] / 100
).sum()

health_score = (
    100
    - (new_default * 2)
    - (customers_rejected / original_customers * 25)
)

health_score = max(0, min(100, health_score))

# -------------------------------------------------------
# KPI CARDS
# -------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Customers Rejected",
    f"{customers_rejected:,}"
)

c2.metric(
    "Risk Reduction",
    f"{risk_reduction:.2f}%"
)

c3.metric(
    "Estimated Interest Revenue",
    f"${estimated_interest:,.0f}"
)

c4.metric(
    "Portfolio Health",
    f"{health_score:.0f}/100"
)

st.markdown("---")

# ============================================================
# BEFORE VS AFTER COMPARISON
# ============================================================

comparison = pd.DataFrame({
    "Metric": [
        "Original",
        "Simulated"
    ],
    "Default Rate": [
        original_default,
        new_default
    ],
    "Approved Customers": [
        original_customers,
        approved_customers
    ]
})

left, right = st.columns(2)

fig7 = px.bar(
    comparison,
    x="Metric",
    y="Default Rate",
    color="Metric",
    text_auto=".2f",
    title="Default Rate Comparison"
)

fig7.update_layout(
    template="plotly_white",
    showlegend=False
)

with left:
    st.plotly_chart(fig7, use_container_width=True)

fig8 = px.bar(
    comparison,
    x="Metric",
    y="Approved Customers",
    color="Metric",
    text_auto=".0f",
    title="Customer Approval Comparison"
)

fig8.update_layout(
    template="plotly_white",
    showlegend=False
)

with right:
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

# ============================================================
# AI DECISION SUMMARY
# ============================================================

st.header("🤖 AI Decision Summary")

summary = []

if risk_reduction > 5:
    summary.append(
        f"✅ The proposed policy reduces the estimated default rate by {risk_reduction:.2f}%."
    )
else:
    summary.append(
        "⚠️ The selected policy provides only a small reduction in default risk."
    )

if approval_rate < 60:
    summary.append(
        "⚠️ Approval rate has become restrictive. Consider relaxing one or more rules."
    )

if estimated_interest > 150000000:
    summary.append(
        "💰 The approved portfolio is expected to generate strong interest revenue."
    )

if health_score >= 80:
    summary.append(
        "🟢 Overall portfolio health is excellent."
    )
elif health_score >= 60:
    summary.append(
        "🟡 Portfolio health is acceptable but can be improved."
    )
else:
    summary.append(
        "🔴 Portfolio health indicates high operational risk."
    )

for item in summary:
    st.success(item)

st.markdown("---")

# ============================================================
# POLICY RECOMMENDATIONS
# ============================================================

st.header("💡 Recommended Lending Actions")

recommendations = []

if minimum_income < 40000:
    recommendations.append(
        "Increase the minimum income threshold to improve borrower quality."
    )

if allow_previous_default:
    recommendations.append(
        "Consider restricting applicants with previous defaults for high-value loans."
    )

if "F" in accepted_grades or "G" in accepted_grades:
    recommendations.append(
        "Review acceptance of Grade F and G loans to reduce future defaults."
    )

if maximum_interest > 18:
    recommendations.append(
        "High-interest loans often indicate higher credit risk. Review pricing policy."
    )

recommendations.append(
    "Compare multiple policy scenarios before implementing changes."
)

for i, rec in enumerate(recommendations, start=1):
    st.info(f"{i}. {rec}")

st.markdown("---")

# ============================================================
# FINAL CONCLUSION
# ============================================================

st.success(
    """
### Executive Conclusion

The simulator transforms historical credit data into an interactive decision-support system.

Managers can experiment with lending policies before implementation and instantly evaluate
their impact on approvals, portfolio value, revenue and credit risk.

This allows better data-driven decision making rather than relying only on historical reports.
"""
)