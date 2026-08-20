import streamlit as st

st.set_page_config(
    page_title="FinSight AI",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 FinSight AI")

st.subheader("Financial Risk Intelligence Platform")

st.markdown("---")

st.markdown("""
## Welcome

FinSight AI is an Executive Decision Support System for banks.

### Modules

- 📊 Executive Dashboard
- 👥 Customer Analytics
- ⚠️ Risk Analytics
- 🧪 Policy Simulator ⭐
- 📋 Executive Report

Use the **left sidebar** to navigate through the modules.
""")

st.success("Select a module from the sidebar to begin.")