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
# SIDEBAR — POLICY CONTROLS
# ============================================================

st.sidebar.header("🎛️ Policy Controls")
st.sidebar.caption("Adjust lending rules and test their portfolio impact.")

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

maximum_interest = st.sidebar.slider(
    "Maximum Interest Rate (%)",
    min_value=float(df["loan_int_rate"].min()),
    max_value=float(df["loan_int_rate"].max()),
    value=float(df["loan_int_rate"].max()),
    step=0.5
)

accepted_grades = st.sidebar.multiselect(
    "Accepted Loan Grades",
    sorted(df["loan_grade"].dropna().unique()),
    default=sorted(df["loan_grade"].dropna().unique())
)

allow_previous_default = st.sidebar.checkbox(
    "Allow Previous Defaulters",
    value=True
)

st.sidebar.markdown("---")

simulate = st.sidebar.button(
    "🚀 Run Policy Simulation",
    use_container_width=True
)


# ============================================================
# DEFAULT STATE
# ============================================================

if "simulation_run" not in st.session_state:
    st.session_state.simulation_run = False

if simulate:
    st.session_state.simulation_run = True


# ============================================================
# POLICY SIMULATION
# ============================================================

if st.session_state.simulation_run:

    policy_df = df.copy()

    # Income rule
    policy_df = policy_df[
        policy_df["person_income"] >= minimum_income
    ]

    # Employment rule
    policy_df = policy_df[
        policy_df["person_emp_length"] >= minimum_employment
    ]

    # Loan grade rule
    policy_df = policy_df[
        policy_df["loan_grade"].isin(accepted_grades)
    ]

    # Interest rate rule
    policy_df = policy_df[
        policy_df["loan_int_rate"] <= maximum_interest
    ]

    # Previous default rule
    if not allow_previous_default:
        policy_df = policy_df[
            policy_df["cb_person_default_on_file"] == "N"
        ]

else:

    # Show original portfolio before simulation
    policy_df = df.copy()


# ============================================================
# SIMULATION STATUS
# ============================================================

if not st.session_state.simulation_run:

    st.info(
        "👈 Configure the lending rules in the sidebar and click "
        "**Run Policy Simulation** to evaluate the proposed policy."
    )

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
# RISK HEATMAP
# ============================================================

st.markdown("---")

st.header("🔥 Risk Concentration Heatmap")

st.caption(
    "Default rate across loan grades and customer income segments."
)

heatmap_df = (
    policy_df
    .groupby(["loan_grade", "income_category"], observed=True)
    .agg(
        Customers=("loan_status", "count"),
        Default_Rate=("loan_status", "mean")
    )
    .reset_index()
)

heatmap_df["Default_Rate"] = (
    heatmap_df["Default_Rate"] * 100
)

heatmap_pivot = heatmap_df.pivot(
    index="loan_grade",
    columns="income_category",
    values="Default_Rate"
)

fig_heatmap = px.imshow(
    heatmap_pivot,
    text_auto=".1f",
    aspect="auto",
    labels={
        "x": "Income Category",
        "y": "Loan Grade",
        "color": "Default Rate (%)"
    },
    title="Default Rate by Loan Grade and Income Category"
)

fig_heatmap.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# ============================================================
# INCOME VS LOAN AMOUNT — RISK SCATTER
# ============================================================

st.markdown("---")

st.header("📈 Borrower Risk Landscape")

st.caption(
    "Explore the relationship between customer income, loan amount "
    "and observed credit risk."
)

scatter_df = policy_df.copy()

scatter_df["Risk Status"] = scatter_df["loan_status"].map(
    {
        0: "No Default",
        1: "Default"
    }
)

fig_scatter = px.scatter(
    scatter_df,
    x="person_income",
    y="loan_amnt",
    color="Risk Status",
    size="loan_amnt",
    hover_data=[
        "loan_grade",
        "loan_intent",
        "loan_int_rate",
        "person_emp_length",
        "income_category"
    ],
    labels={
        "person_income": "Annual Income ($)",
        "loan_amnt": "Loan Amount ($)"
    },
    title="Income vs Loan Amount by Default Status",
    opacity=0.65
)

fig_scatter.update_layout(
    template="plotly_white",
    height=550
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)
# ============================================================
# AUTOMATED VISUAL INSIGHT
# ============================================================

st.markdown("---")

st.header("🧠 Key Visual Insight")

if len(policy_df) > 0:

    highest_risk_group = (
        heatmap_df
        .sort_values("Default_Rate", ascending=False)
        .iloc[0]
    )

    st.info(
        f"""
        **Highest observed-risk segment:** 
        Loan Grade **{highest_risk_group['loan_grade']}** combined with
        **{highest_risk_group['income_category']}** income category.

        Observed default rate in this segment:
        **{highest_risk_group['Default_Rate']:.2f}%**

        This segment can be investigated further before expanding lending
        exposure to similar borrowers.
        """
    )

else:

    st.warning(
        "No customers satisfy the selected policy. "
        "Relax one or more policy conditions."
    )

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

# ============================================================
# PORTFOLIO IMPACT KPIs
# ============================================================

approved = len(policy_df)

approval_rate = (
    approved / len(df) * 100
    if len(df) > 0 else 0
)

portfolio_value = policy_df["loan_amnt"].sum()

estimated_default = (
    policy_df["loan_status"].mean() * 100
    if approved > 0 else 0
)

original_default = df["loan_status"].mean() * 100

default_change = estimated_default - original_default


st.markdown("### 📊 Simulated Portfolio")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Eligible Customers",
        f"{approved:,}",
        f"{approved - len(df):+,}"
    )

with c2:
    st.metric(
        "Approval Rate",
        f"{approval_rate:.2f}%"
    )

with c3:
    st.metric(
        "Loan Exposure",
        f"${portfolio_value:,.0f}"
    )

with c4:
    st.metric(
        "Estimated Default Rate",
        f"{estimated_default:.2f}%",
        f"{default_change:+.2f}%"
    )

# ============================================================
# BEFORE VS SIMULATED PORTFOLIO
# ============================================================

st.markdown("---")

st.header("🔄 Policy Impact Comparison")

original_customers = len(df)
simulated_customers = len(policy_df)

original_loan_value = df["loan_amnt"].sum()
simulated_loan_value = policy_df["loan_amnt"].sum()

original_default = df["loan_status"].mean() * 100

simulated_default = (
    policy_df["loan_status"].mean() * 100
    if len(policy_df) > 0 else 0
)

comparison = pd.DataFrame({
    "Metric": [
        "Customers",
        "Loan Exposure",
        "Default Rate"
    ],
    "Current Portfolio": [
        original_customers,
        original_loan_value,
        original_default
    ],
    "Simulated Portfolio": [
        simulated_customers,
        simulated_loan_value,
        simulated_default
    ]
})

left, right = st.columns(2)

with left:

    fig_customers = px.bar(
        comparison,
        x="Metric",
        y="Current Portfolio",
        title="Current Portfolio",
        text_auto=".2s"
    )

    fig_customers.update_layout(
        template="plotly_white",
        showlegend=False,
        height=380
    )

    st.plotly_chart(
        fig_customers,
        use_container_width=True
    )


with right:

    fig_simulated = px.bar(
        comparison,
        x="Metric",
        y="Simulated Portfolio",
        title="Simulated Portfolio",
        text_auto=".2s"
    )

    fig_simulated.update_layout(
        template="plotly_white",
        showlegend=False,
        height=380
    )

    st.plotly_chart(
        fig_simulated,
        use_container_width=True
    )

# ============================================================
# AI DECISION SUMMARY
# ============================================================

st.header("🧠 Decision Intelligence Summary")

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