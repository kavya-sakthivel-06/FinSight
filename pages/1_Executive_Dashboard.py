import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="FinSight AI | Executive Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# THEME / CUSTOM CSS
# =========================================================
# Palette: deep navy background, electric teal + amber accents,
# card-based layout with soft shadows and rounded corners.

PRIMARY = "#00D4B4"      # teal accent
SECONDARY = "#FFB020"    # amber accent
DANGER = "#FF5C5C"
BG_DARK = "#0B0F19"
CARD_BG = "#141B2D"
CARD_BORDER = "#232B3E"
TEXT_MUTED = "#8B94A8"

st.markdown(f"""
<style>
    /* ---------- Global ---------- */
    .stApp {{
        background-color: {BG_DARK};
        color: #E6E8EC;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {CARD_BG};
        border-right: 1px solid {CARD_BORDER};
    }}

    /* ---------- Hide default Streamlit chrome ---------- */
    #MainMenu, footer {{visibility: hidden;}}

    /* ---------- Headers ---------- */
    h1, h2, h3, h4 {{
        color: #F4F6F9 !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }}

    /* ---------- KPI Card ---------- */
    .kpi-card {{
        background: linear-gradient(145deg, {CARD_BG}, #10162700);
        border: 1px solid {CARD_BORDER};
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        transition: transform 0.15s ease, border 0.15s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-3px);
        border: 1px solid {PRIMARY};
    }}
    .kpi-label {{
        font-size: 13px;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 6px;
        font-weight: 600;
    }}
    .kpi-value {{
        font-size: 28px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
    }}
    .kpi-delta-up {{ color: {PRIMARY}; font-size: 13px; font-weight: 600; }}
    .kpi-delta-down {{ color: {DANGER}; font-size: 13px; font-weight: 600; }}
    .kpi-icon {{
        font-size: 22px;
        opacity: 0.85;
    }}

    /* ---------- Section card wrapper ---------- */
    .section-card {{
        background-color: {CARD_BG};
        border: 1px solid {CARD_BORDER};
        border-radius: 16px;
        padding: 20px 22px;
        margin-bottom: 18px;
    }}

    /* ---------- Health score badge ---------- */
    .health-badge {{
        display: inline-block;
        padding: 6px 16px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
    }}

    /* ---------- Pills for recommendations / alerts ---------- */
    .pill {{
        display: flex;
        align-items: flex-start;
        gap: 10px;
        background-color: #10162A;
        border-left: 3px solid {PRIMARY};
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-size: 14px;
        color: #DDE1EA;
    }}
    .pill-warn {{ border-left-color: {SECONDARY}; }}
    .pill-danger {{ border-left-color: {DANGER}; }}

    /* ---------- Divider ---------- */
    .thin-divider {{
        height: 1px;
        background: {CARD_BORDER};
        margin: 28px 0;
        border: none;
    }}

    /* ---------- Sidebar header ---------- */
    .sidebar-title {{
        font-size: 20px;
        font-weight: 800;
        color: {PRIMARY};
        margin-bottom: 2px;
    }}
    .sidebar-subtitle {{
        font-size: 12px;
        color: {TEXT_MUTED};
        margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================

def kpi_card(icon, label, value, delta=None, delta_positive=True):
    """Render a single KPI as a styled HTML card."""
    delta_html = ""
    if delta is not None:
        cls = "kpi-delta-up" if delta_positive else "kpi-delta-down"
        arrow = "▲" if delta_positive else "▼"
        delta_html = f'<div class="{cls}">{arrow} {delta}</div>'

    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


def section_header(icon, title, subtitle=None):
    sub_html = f'<div style="color:{TEXT_MUTED}; font-size:13px; margin-top:-6px;">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
        <div style="margin-top:8px; margin-bottom:14px;">
            <h3 style="margin-bottom:0;">{icon} {title}</h3>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)


# A single shared Plotly theme so every chart looks consistent
def style_fig(fig, title=None, showlegend=True):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color="#DDE1EA", family="Inter, Segoe UI, sans-serif"),
        title=dict(text=title, font=dict(size=16, color="#F4F6F9")) if title else None,
        showlegend=showlegend,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=50, b=10),
        colorway=[PRIMARY, SECONDARY, "#5C8DFF", "#FF7A9C", "#8B94A8", "#B48CFF"]
    )
    fig.update_xaxes(gridcolor=CARD_BORDER, zerolinecolor=CARD_BORDER)
    fig.update_yaxes(gridcolor=CARD_BORDER, zerolinecolor=CARD_BORDER)
    return fig


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/credit_risk_cleaned.csv")
    return df

df = load_data()

# =========================================================
# SIDEBAR — FILTERS
# =========================================================

st.sidebar.markdown('<div class="sidebar-title">🏦 FinSight AI</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-subtitle">Credit Risk Intelligence Platform</div>', unsafe_allow_html=True)

st.sidebar.markdown("### 🔎 Filters")

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

st.sidebar.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
st.sidebar.caption("Data refreshed on load · cached for performance")

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df["loan_intent"].isin(loan_purpose)) &
    (df["loan_grade"].isin(loan_grade)) &
    (df["person_home_ownership"].isin(home)) &
    (df["risk_label"].isin(risk))
]

if filtered_df.empty:
    st.warning("No records match the current filter selection. Adjust filters in the sidebar.")
    st.stop()

# =========================================================
# HEADER
# =========================================================

st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
    <div>
        <h1 style="margin-bottom:0;">Executive Financial Dashboard</h1>
        <div style="color:{TEXT_MUTED}; font-size:14px;">
            Interactive overview of customer portfolio, lending patterns and credit risk
        </div>
    </div>
    <div style="text-align:right; color:{TEXT_MUTED}; font-size:13px;">
        Records in view<br>
        <span style="color:{PRIMARY}; font-size:20px; font-weight:800;">{len(filtered_df):,}</span>
    </div>
</div>
<hr class="thin-divider">
""", unsafe_allow_html=True)

# =========================================================
# KPI ROW
# =========================================================

total_customers = len(filtered_df)
total_loans = filtered_df["loan_amnt"].sum()
avg_income = filtered_df["person_income"].mean()
avg_interest = filtered_df["loan_int_rate"].mean()
default_rate = filtered_df["loan_status"].mean() * 100

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    kpi_card("👥", "Customers", f"{total_customers:,}")
with k2:
    kpi_card("💰", "Total Loan Value", f"${total_loans:,.0f}")
with k3:
    kpi_card("📈", "Avg. Income", f"${avg_income:,.0f}")
with k4:
    default_bad = default_rate > 15
    kpi_card("⚠️", "Default Rate", f"{default_rate:.2f}%",
              delta="Elevated" if default_bad else "Healthy",
              delta_positive=not default_bad)
with k5:
    kpi_card("💵", "Avg. Interest Rate", f"{avg_interest:.2f}%")

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# =========================================================
# TABS — organize dense content instead of one long scroll
# =========================================================

tab_overview, tab_demo, tab_risk, tab_decision = st.tabs(
    ["📊 Portfolio Overview", "👤 Customer Demographics", "🚨 Risk & Alerts", "🧠 Decision Support"]
)

# ---------------------------------------------------------
# TAB 1: PORTFOLIO OVERVIEW
# ---------------------------------------------------------
with tab_overview:
    section_header("📊", "Lending Portfolio", "How loans break down by purpose, grade, and size")

    c1, c2 = st.columns(2)

    loan_counts = filtered_df["loan_intent"].value_counts().reset_index()
    loan_counts.columns = ["Loan Purpose", "Customers"]
    fig1 = px.bar(loan_counts, x="Loan Purpose", y="Customers", color="Loan Purpose", text="Customers")
    fig1 = style_fig(fig1, "Loan Purpose Distribution", showlegend=False)
    c1.plotly_chart(fig1, use_container_width=True)

    grade_counts = filtered_df["loan_grade"].value_counts().reset_index()
    grade_counts.columns = ["Grade", "Customers"]
    fig2 = px.pie(grade_counts, names="Grade", values="Customers", hole=0.55)
    fig2 = style_fig(fig2, "Loan Grade Distribution")
    c2.plotly_chart(fig2, use_container_width=True)

    loan_size_df = filtered_df["loan_size"].value_counts().reset_index()
    loan_size_df.columns = ["Loan Size", "Customers"]
    fig9 = px.bar(loan_size_df, x="Loan Size", y="Customers", color="Loan Size", text="Customers")
    fig9 = style_fig(fig9, "Loan Size Distribution", showlegend=False)
    st.plotly_chart(fig9, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: CUSTOMER DEMOGRAPHICS
# ---------------------------------------------------------
with tab_demo:
    section_header("👤", "Customer Demographics", "Who the portfolio's customers are")

    c3, c4 = st.columns(2)

    home_df = filtered_df["person_home_ownership"].value_counts().reset_index()
    home_df.columns = ["Home Ownership", "Customers"]
    fig3 = px.pie(home_df, names="Home Ownership", values="Customers", hole=0.55)
    fig3 = style_fig(fig3, "Home Ownership Distribution")
    c3.plotly_chart(fig3, use_container_width=True)

    age_df = filtered_df["age_group"].value_counts().reset_index()
    age_df.columns = ["Age Group", "Customers"]
    fig4 = px.bar(age_df, x="Age Group", y="Customers", color="Age Group", text="Customers")
    fig4 = style_fig(fig4, "Customer Age Groups", showlegend=False)
    c4.plotly_chart(fig4, use_container_width=True)

    c5, c6 = st.columns(2)

    income_df = filtered_df["income_category"].value_counts().reset_index()
    income_df.columns = ["Income Category", "Customers"]
    fig5 = px.bar(income_df, x="Income Category", y="Customers", color="Income Category", text="Customers")
    fig5 = style_fig(fig5, "Income Category Distribution", showlegend=False)
    c5.plotly_chart(fig5, use_container_width=True)

    employment_df = filtered_df["employment_category"].value_counts().reset_index()
    employment_df.columns = ["Employment Category", "Customers"]
    fig8 = px.bar(employment_df, x="Employment Category", y="Customers", color="Employment Category", text="Customers")
    fig8 = style_fig(fig8, "Employment Category", showlegend=False)
    c6.plotly_chart(fig8, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: RISK & ALERTS
# ---------------------------------------------------------
with tab_risk:
    section_header("🚨", "Risk Profile", "Where credit risk concentrates in the current portfolio")

    c7, c8 = st.columns(2)

    risk_df = filtered_df["risk_label"].value_counts().reset_index()
    risk_df.columns = ["Risk Label", "Customers"]
    fig6 = px.bar(risk_df, x="Risk Label", y="Customers", color="Risk Label", text="Customers")
    fig6 = style_fig(fig6, "Risk Category", showlegend=False)
    c7.plotly_chart(fig6, use_container_width=True)

    interest_df = filtered_df["interest_category"].value_counts().reset_index()
    interest_df.columns = ["Interest Category", "Customers"]
    fig7 = px.pie(interest_df, names="Interest Category", values="Customers", hole=0.55)
    fig7 = style_fig(fig7, "Interest Rate Categories")
    c8.plotly_chart(fig7, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("📢", "Portfolio Alerts")

    if default_rate >= 25:
        st.markdown(f'<div class="pill pill-danger">🔴 <b>High default rate detected</b> — immediate review of lending policy recommended.</div>', unsafe_allow_html=True)
    elif default_rate >= 15:
        st.markdown(f'<div class="pill pill-warn">🟠 <b>Moderate default rate observed</b> — monitor customer segments closely.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="pill">🟢 <b>Default rate within acceptable limits.</b></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 4: DECISION SUPPORT
# ---------------------------------------------------------
with tab_decision:
    section_header("🧠", "Executive Decision Support", "Health score, insights, and recommended actions")

    # ---- Portfolio Health Score ----
    score = 100
    score -= default_rate * 2
    score -= avg_interest
    score += avg_income / 5000
    score = max(0, min(100, score))

    if score >= 80:
        health, color = "Excellent", PRIMARY
    elif score >= 60:
        health, color = "Good", "#7ED957"
    elif score >= 40:
        health, color = "Moderate Risk", SECONDARY
    else:
        health, color = "High Risk", DANGER

    hc1, hc2 = st.columns([1, 2])
    with hc1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number={'suffix': "/100", 'font': {'color': '#F4F6F9', 'size': 34}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': TEXT_MUTED},
                'bar': {'color': color},
                'bgcolor': CARD_BG,
                'bordercolor': CARD_BORDER,
                'steps': [
                    {'range': [0, 40], 'color': '#2A1520'},
                    {'range': [40, 60], 'color': '#2A2415'},
                    {'range': [60, 80], 'color': '#122A1E'},
                    {'range': [80, 100], 'color': '#0F2A26'},
                ],
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor=CARD_BG, font=dict(color="#DDE1EA"),
            margin=dict(l=20, r=20, t=20, b=10), height=260
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown(f'<div style="text-align:center;"><span class="health-badge" style="background-color:{color}22; color:{color};">{health}</span></div>', unsafe_allow_html=True)

    with hc2:
        most_purpose = filtered_df["loan_intent"].mode()[0]
        most_grade = filtered_df["loan_grade"].mode()[0]
        most_risk = filtered_df["risk_label"].mode()[0]
        most_income = filtered_df["income_category"].mode()[0]

        ic1, ic2 = st.columns(2)
        with ic1:
            st.markdown(f"""
            <div class="section-card">
                <b>📋 Portfolio Summary</b><br><br>
                Customers Analysed: <b>{len(filtered_df):,}</b><br>
                Most Common Purpose: <b>{most_purpose}</b><br>
                Dominant Loan Grade: <b>{most_grade}</b><br>
                Avg. Customer Income: <b>${avg_income:,.0f}</b><br>
                Avg. Interest Rate: <b>{avg_interest:.2f}%</b>
            </div>
            """, unsafe_allow_html=True)
        with ic2:
            st.markdown(f"""
            <div class="section-card">
                <b>⚠️ Risk Summary</b><br><br>
                Default Rate: <b>{default_rate:.2f}%</b><br>
                Dominant Risk Category: <b>{most_risk}</b><br>
                Largest Income Segment: <b>{most_income}</b><br>
                Portfolio Health: <b style="color:{color};">{health}</b>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

    # ---- Smart Recommendations ----
    section_header("💡", "Smart Recommendations")

    recommendations = []
    if default_rate > 20:
        recommendations.append("Increase minimum income requirement to reduce default risk.")
    if avg_interest > 15:
        recommendations.append("Review lending strategy — customers are paying relatively high interest.")
    if most_grade in ["E", "F", "G"]:
        recommendations.append("Large proportion of lower-grade loans detected. Strengthen credit evaluation.")
    if most_risk == "High Risk":
        recommendations.append("Increase monitoring of high-risk customers and tighten approval criteria.")
    if avg_income < 50000:
        recommendations.append("Portfolio contains many lower-income applicants. Review affordability checks.")
    if not recommendations:
        recommendations.append("Current portfolio appears stable. Continue monitoring key financial indicators.")

    for i, rec in enumerate(recommendations, start=1):
        st.markdown(f'<div class="pill">✅ <b>{i}.</b> {rec}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

    with st.expander("📖 About this Dashboard"):
        st.write("""
This Executive Dashboard is one module of the **FinSight AI – Executive Decision Support System
for Credit Risk Management**.

The dashboard enables decision makers to:
- Monitor customer portfolios
- Analyse lending patterns
- Evaluate credit risk
- Understand customer demographics
- Support lending decisions through interactive visualisations

Unlike traditional dashboards that only display historical data, this platform is designed to
support business decisions and will be extended with a Loan Approval Policy Simulator.
""")