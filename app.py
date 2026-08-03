import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FinSight AI",
    
    layout="wide"
)

df = pd.read_csv("data/processed/credit_risk_cleaned.csv")

st.title("🏦 FinSight AI")
st.subheader("Executive Financial Risk Dashboard")

total_customers = len(df)
total_loan = df["loan_amnt"].sum()
average_income = df["person_income"].mean()
default_rate = df["loan_status"].mean() * 100
average_interest = df["loan_int_rate"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("👥 Customers", f"{total_customers:,}")

col2.metric("💰 Total Loan", f"${total_loan:,.0f}")

col3.metric("📈 Avg Income", f"${average_income:,.0f}")

col4.metric("⚠ Default Rate", f"{default_rate:.2f}%")

col5.metric("💵 Avg Interest", f"{average_interest:.2f}%")

import plotly.express as px

loan_purpose = (
    df["loan_intent"]
    .value_counts()
    .reset_index()
)

loan_purpose.columns = ["Loan Purpose", "Count"]

fig = px.bar(
    loan_purpose,
    x="Loan Purpose",
    y="Count",
    color="Loan Purpose",
    title="Loan Purpose Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.sidebar.title("🏦 FinSight AI")

st.sidebar.header("Filters")

loan_type = st.sidebar.multiselect(
    "Loan Purpose",
    options=sorted(df["loan_intent"].unique()),
    default=sorted(df["loan_intent"].unique())
)

grade = st.sidebar.multiselect(
    "Loan Grade",
    options=sorted(df["loan_grade"].unique()),
    default=sorted(df["loan_grade"].unique())
)

filtered_df = df[
    (df["loan_intent"].isin(loan_type)) &
    (df["loan_grade"].isin(grade))
]
col1, col2 = st.columns(2)
loan_purpose = (
    filtered_df["loan_intent"]
    .value_counts()
    .reset_index()
)

loan_purpose.columns = ["Loan Purpose", "Count"]

fig1 = px.bar(
    loan_purpose,
    x="Loan Purpose",
    y="Count",
    color="Loan Purpose",
    title="Loan Purpose Distribution"
)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

    loan_grade = (
    filtered_df["loan_grade"]
    .value_counts()
    .reset_index()
)

loan_grade.columns = ["Grade", "Count"]

fig2 = px.pie(
    loan_grade,
    names="Grade",
    values="Count",
    title="Loan Grade Distribution"
)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
fig3 = px.pie(
    filtered_df,
    names="person_home_ownership",
    title="Home Ownership"
)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

fig4 = px.histogram(
    filtered_df,
    x="person_age",
    nbins=25,
    title="Customer Age Distribution"
)

with col4:
    st.plotly_chart(fig4, use_container_width=True)
st.subheader("🧠 Executive Insights")

most_common_purpose = filtered_df["loan_intent"].mode()[0]
most_common_grade = filtered_df["loan_grade"].mode()[0]
default_rate = filtered_df["loan_status"].mean() * 100

st.info(f"""
• Most common loan purpose: **{most_common_purpose}**

• Most frequent loan grade: **{most_common_grade}**

• Overall default rate: **{default_rate:.2f}%**

• Total customers analysed: **{len(filtered_df):,}**
""")