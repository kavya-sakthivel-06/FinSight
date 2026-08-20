import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="👥",
    layout="wide"
)


# --------------------------------------------------------
# LOAD DATA
# --------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/credit_risk_cleaned.csv"
    )


df = load_data()


# --------------------------------------------------------
# FIX DATA TYPES
# --------------------------------------------------------

categorical_columns = [
    "income_category",
    "age_group",
    "employment_category",
    "person_home_ownership",
    "loan_intent",
    "loan_grade",
    "risk_label"
]


for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown").astype(str)



# --------------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------------

st.sidebar.title("👥 Customer Analytics")


income_options = sorted(
    df["income_category"].unique().tolist()
)

income_filter = st.sidebar.multiselect(
    "Income Category",
    options=income_options,
    default=income_options
)



age_options = sorted(
    df["age_group"].unique().tolist()
)

age_filter = st.sidebar.multiselect(
    "Age Group",
    options=age_options,
    default=age_options
)



employment_options = sorted(
    df["employment_category"].unique().tolist()
)

employment_filter = st.sidebar.multiselect(
    "Employment Category",
    options=employment_options,
    default=employment_options
)



home_options = sorted(
    df["person_home_ownership"].unique().tolist()
)

home_filter = st.sidebar.multiselect(
    "Home Ownership",
    options=home_options,
    default=home_options
)



# --------------------------------------------------------
# FILTER DATA
# --------------------------------------------------------

filtered_df = df[
    (df["income_category"].isin(income_filter)) &
    (df["age_group"].isin(age_filter)) &
    (df["employment_category"].isin(employment_filter)) &
    (df["person_home_ownership"].isin(home_filter))
]



filtered_df = df[
    (df["income_category"].isin(income_filter)) &
    (df["age_group"].isin(age_filter)) &
    (df["employment_category"].isin(employment_filter)) &
    (df["person_home_ownership"].isin(home_filter))
]

# --------------------------------------------------------
# TITLE
# --------------------------------------------------------

st.title("👥 Customer Analytics")

st.markdown(
    "Understand customer demographics, income patterns, employment, and borrowing behaviour."
)

st.markdown("---")

# --------------------------------------------------------
# KPI CARDS
# --------------------------------------------------------

customers = len(filtered_df)
avg_income = filtered_df["person_income"].mean()
avg_age = filtered_df["person_age"].mean()
avg_emp = filtered_df["person_emp_length"].mean()
loan_amount = filtered_df["loan_amnt"].mean()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Customers", f"{customers:,}")
c2.metric("Average Income", f"${avg_income:,.0f}")
c3.metric("Average Age", f"{avg_age:.1f} Years")
c4.metric("Employment", f"{avg_emp:.1f} Years")
c5.metric("Average Loan", f"${loan_amount:,.0f}")

st.markdown("---")

# --------------------------------------------------------
# AGE DISTRIBUTION
# --------------------------------------------------------

left, right = st.columns(2)

fig1 = px.histogram(
    filtered_df,
    x="person_age",
    nbins=20,
    color="age_group",
    title="Age Distribution"
)

fig1.update_layout(template="plotly_white")

with left:
    st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------------
# INCOME DISTRIBUTION
# --------------------------------------------------------

fig2 = px.histogram(
    filtered_df,
    x="person_income",
    nbins=30,
    color="income_category",
    title="Income Distribution"
)

fig2.update_layout(template="plotly_white")

with right:
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
# ============================================================
# HOME OWNERSHIP & EMPLOYMENT ANALYSIS
# ============================================================

st.subheader("🏠 Home Ownership & Employment")

col1, col2 = st.columns(2)

# -----------------------------
# Home Ownership
# -----------------------------

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
    hole=0.45,
    title="Home Ownership Distribution"
)

fig3.update_layout(template="plotly_white")

with col1:
    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Employment Category
# -----------------------------

emp_df = (
    filtered_df["employment_category"]
    .value_counts()
    .reset_index()
)

emp_df.columns = ["Employment Category", "Customers"]

fig4 = px.bar(
    emp_df,
    x="Employment Category",
    y="Customers",
    color="Employment Category",
    text="Customers",
    title="Employment Category"
)

fig4.update_layout(
    showlegend=False,
    template="plotly_white"
)

with col2:
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ============================================================
# INCOME CATEGORY & LOAN PURPOSE
# ============================================================

st.subheader("💰 Income & Borrowing Behaviour")

col3, col4 = st.columns(2)

# -----------------------------
# Income Category
# -----------------------------

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

with col3:
    st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# Loan Purpose
# -----------------------------

loan_df = (
    filtered_df["loan_intent"]
    .value_counts()
    .reset_index()
)

loan_df.columns = ["Loan Purpose", "Customers"]

fig6 = px.bar(
    loan_df,
    x="Loan Purpose",
    y="Customers",
    color="Loan Purpose",
    text="Customers",
    title="Loan Purpose Distribution"
)

fig6.update_layout(
    showlegend=False,
    template="plotly_white",
    xaxis_tickangle=-20
)

with col4:
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# ============================================================
# AGE GROUP VS LOAN PURPOSE
# ============================================================

st.subheader("📊 Customer Segmentation")

segment = (
    filtered_df.groupby(["age_group", "loan_intent"])
    .size()
    .reset_index(name="Customers")
)

fig7 = px.sunburst(
    segment,
    path=["age_group", "loan_intent"],
    values="Customers",
    title="Age Group → Loan Purpose"
)

fig7.update_layout(template="plotly_white")

st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")
# ============================================================
# CUSTOMER PROFILE SUMMARY
# ============================================================

st.header("🧠 Customer Intelligence")

most_income = filtered_df["income_category"].mode()[0]
most_age = filtered_df["age_group"].mode()[0]
most_home = filtered_df["person_home_ownership"].mode()[0]
most_employment = filtered_df["employment_category"].mode()[0]
most_loan = filtered_df["loan_intent"].mode()[0]

left, right = st.columns(2)

with left:

    st.info(f"""
### Customer Profile

👥 Customers Analysed

**{len(filtered_df):,}**

💰 Average Income

**${filtered_df["person_income"].mean():,.0f}**

🎂 Average Age

**{filtered_df["person_age"].mean():.1f} Years**

🏠 Dominant Home Ownership

**{most_home}**
""")

with right:

    st.success(f"""
### Behaviour Summary

Largest Income Group

**{most_income}**

Largest Age Group

**{most_age}**

Employment Category

**{most_employment}**

Most Common Loan Purpose

**{most_loan}**
""")

st.markdown("---")

# ============================================================
# CUSTOMER PERSONAS
# ============================================================

st.header("👤 Customer Personas")

high_income = len(filtered_df[filtered_df["income_category"]=="High"])
medium_income = len(filtered_df[filtered_df["income_category"]=="Medium"])
low_income = len(filtered_df[filtered_df["income_category"]=="Low"])

c1, c2, c3 = st.columns(3)

c1.metric("High Income", high_income)
c2.metric("Medium Income", medium_income)
c3.metric("Low Income", low_income)

st.markdown("---")

# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.header("📊 Executive Insights")

insights = []

if filtered_df["person_income"].mean() > 70000:
    insights.append(
        "The customer portfolio is dominated by higher-income applicants."
    )
else:
    insights.append(
        "The customer portfolio contains a significant number of lower-income applicants."
    )

if filtered_df["person_emp_length"].mean() > 5:
    insights.append(
        "Customers generally have stable employment histories."
    )
else:
    insights.append(
        "Many applicants have relatively short employment histories."
    )

if most_home == "RENT":
    insights.append(
        "Rental housing is the most common home ownership category."
    )
else:
    insights.append(
        "Most customers own or finance their homes."
    )

if most_loan == "EDUCATION":
    insights.append(
        "Education loans are the largest lending segment."
    )

if most_loan == "PERSONAL":
    insights.append(
        "Personal loans account for the largest share of applications."
    )

if most_loan == "MEDICAL":
    insights.append(
        "Medical loans form a significant portion of the lending portfolio."
    )

for i, insight in enumerate(insights, start=1):
    st.success(f"{i}. {insight}")

st.markdown("---")

# ============================================================
# RECOMMENDATIONS
# ============================================================

st.header("💡 Recommendations")

recommendations = []

if filtered_df["person_income"].mean() < 50000:
    recommendations.append(
        "Review affordability assessment for lower-income applicants."
    )

if filtered_df["person_emp_length"].mean() < 2:
    recommendations.append(
        "Introduce additional employment verification for applicants with limited work experience."
    )

recommendations.append(
    "Use customer segmentation to personalize lending strategies."
)

recommendations.append(
    "Monitor income groups and loan purposes continuously for changing demand."
)

recommendations.append(
    "Combine customer analytics with risk analytics before approving high-value loans."
)

for rec in recommendations:
    st.info("✔ " + rec)

st.markdown("---")

# ============================================================
# PAGE FOOTER
# ============================================================

st.caption("""
Customer Analytics is a core module of FinSight AI.
It provides demographic and behavioural insights that support better lending decisions.
""")