# app.py
import streamlit as st
import pandas as pd
import os
import json
import anthropic
import PyPDF2
from io import BytesIO
from database import DatabaseManager
from prompts import get_contract_analysis_prompt, get_tco_pricing_prompt
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Commercial Manager Assistant",
    page_icon="🚀",
    layout="wide"
)

# --- GLOBAL STYLES (Updated based on the new research report) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Open+Sans:wght@400;600&display=swap');
    
    /* NEW COLOR PALETTE from the report */
    :root {
        --primary-color: #1E3A8A;      /* Professional Blue */
        --secondary-color: #3B82F6;   /* Brighter Blue for interactions */
        --accent-color: #EA6A47;       /* Professional Orange for highlights */
        --background-main: #F8F9FA;
        --background-module: #FFFFFF;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --border-color: #E5E7EB;
        --success-color: #10B981;
        --warning-color: #F59E0B;
        --error-color: #EF4444;
    }

    body { font-family: 'Open Sans', sans-serif; }
    .main .block-container { padding-top: 1rem; padding-bottom: 2rem; }
    h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif; font-weight: 700; color: var(--primary-color); }
    
    .stButton>button {
        background-color: var(--secondary-color);
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: var(--primary-color);
        color: white;
    }
    .st-emotion-cache-1h9d2c2 { /* Expander styling */
        border-color: var(--border-color) !important;
    }
</style>
""", unsafe_allow_html=True)


# --- INITIALIZATION ---
@st.cache_resource
def init_db_manager():
    return DatabaseManager()

@st.cache_resource
def init_anthropic_client():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found! Check your .env file.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)

db = init_db_manager()
client = init_anthropic_client()

# --- UTILITY & SETUP FUNCTIONS ---
def extract_text_from_pdf(file_bytes):
    try:
        reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        return "".join(page.extract_text() for page in reader.pages)
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

def setup_database():
    if 'db_initialized' not in st.session_state:
        db.initialize_database()
        st.session_state.db_initialized = True

# --- PAGE RENDERERS ---

def render_main_dashboard():
    """Renders the new main dashboard with quick-access widgets, as per the report."""
    st.title("Commercial Manager Dashboard")
    st.write(f"Welcome back, Abdülkerim. Here's your daily overview.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Contracts Requiring Attention", icon="📄")
        expiring_contracts = db.get_expiring_contracts()
        if not expiring_contracts.empty:
            for index, row in expiring_contracts.iterrows():
                st.write(f"- **{row['contract_title']}** expires on {row['expiration_date'].strftime('%Y-%m-%d')}")
        else:
            st.write("No contracts expiring soon.")
            
    with col2:
        st.warning("High-Priority Tasks", icon="⚠️")
        st.write("- Follow up on 'FutureNet VoNR RFP' (Deadline: 15 days)")
        st.write("- Review liability clause in 'InnovateTel' renewal")

    with col3:
        st.success("Quarterly KPIs", icon="🏆")
        kpi_data = db.get_kpi_summary()
        win_rate_data = kpi_data.get('win_rate', {'value': 0, 'change': 0})
        margin_data = kpi_data.get('avg_margin', {'value': 0, 'change': 0})
        st.metric("Win Rate", f"{win_rate_data['value']}%", f"{win_rate_data['change']}%")
        st.metric("Avg. Deal Margin", f"{margin_data['value']}%", f"{margin_data['change']}%")
        
    st.markdown("---")
    st.subheader("Quick Actions")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    if q_col1.button("Analyze New Contract", use_container_width=True): st.session_state.page = "Contract Lifecycle Management"; st.rerun()
    if q_col2.button("Run a TCO Analysis", use_container_width=True): st.session_state.page = "TCO & Pricing Optimization"; st.rerun()
    if q_col3.button("View Partner Portal", use_container_width=True): st.session_state.page = "Partner & Reseller Portal"; st.rerun()
    if q_col4.button("Assess an RFx", use_container_width=True): st.session_state.page = "RFx Response Automation"; st.rerun()

def render_contract_page():
    st.markdown("### 📄 AI Contract Lifecycle Management")
    st.write("Upload a contract to perform AI-driven risk analysis and automatically save key terms to the database.")

    with st.container(border=True):
        st.subheader("New Contract Analysis")
        with st.form("contract_analysis_form"):
            contract_title = st.text_input("Contract Title*", placeholder="e.g., MSA with FutureNet Mobile")
            contract_type = st.selectbox("Contract Type*", ["Reseller Agreement", "MSA", "NDA", "Partnership Agreement"])
            uploaded_file = st.file_uploader("Upload Contract PDF*", type=['pdf'], label_visibility="collapsed")
            submitted = st.form_submit_button("Analyze Contract & Save", type="primary", use_container_width=True)

            if submitted and uploaded_file and contract_title:
                with st.spinner("Reading PDF & performing AI analysis..."):
                    contract_text = extract_text_from_pdf(uploaded_file.getvalue())
                    if contract_text:
                        prompt = get_contract_analysis_prompt(contract_text, contract_type)
                        try:
                            message = client.messages.create(model="claude-3-sonnet-20240229", max_tokens=2048, messages=[{"role": "user", "content": prompt}]).content[0].text
                            analysis_result = json.loads(message)
                            contract_id = db.save_contract_and_analysis(contract_title, contract_type, analysis_result)
                            st.success(f"Contract '{contract_title}' (ID: {contract_id}) analyzed and saved!")
                            st.session_state.analysis_result = analysis_result
                        except Exception as e:
                            st.error(f"An error occurred: {e}")
            elif submitted:
                st.warning("Please provide a title and upload a PDF.")
    
    if 'analysis_result' in st.session_state:
        with st.expander("View Last AI Analysis Results", expanded=True):
            result = st.session_state.analysis_result
            st.subheader("AI Risk Analysis")
            for risk in result.get('risk_analysis', []):
                st.error(f"**{risk['risk_level']} Risk:** {risk['clause_category']}")
                st.info(f"**Summary:** {risk['summary']}")
            
            st.subheader("Extracted Key Commercial Terms")
            key_terms_df = pd.DataFrame(result.get('key_terms', {}).items(), columns=['Term', 'Value'])
            st.table(key_terms_df)

    st.subheader("Contract Database")
    if st.button("Refresh Contract List"):
        st.rerun()

    df_contracts = db.get_contracts()
    if not df_contracts.empty:
        df_contracts_with_action = df_contracts.copy()
        df_contracts_with_action['Analyze TCO'] = [False] * len(df_contracts_with_action)
        
        edited_df = st.data_editor(
            df_contracts_with_action, 
            column_config={"ID": st.column_config.Column(disabled=True), "Analyze TCO": st.column_config.CheckboxColumn(default=False)},
            disabled=list(df_contracts.columns),
            hide_index=True, use_container_width=True
        )
        
        selected_row = edited_df[edited_df['Analyze TCO']]
        if not selected_row.empty:
            company_name = selected_row.iloc[0]['Counterparty']
            st.toast(f"Navigating to TCO module for {company_name}...")
            st.session_state.page = "TCO & Pricing Optimization"
            st.session_state.company_for_tco = company_name
            st.rerun()

def render_tco_page():
    st.markdown("### 📊 TCO & Pricing Optimization Tool")
    if 'company_for_tco' in st.session_state:
        st.info(f"Preparing TCO analysis for: **{st.session_state.company_for_tco}**")
        del st.session_state.company_for_tco

    with st.container(border=True):
        st.subheader("TCO Calculator (5-Year)")
        tco_cols = st.columns(3)
        with tco_cols[0]:
            st.markdown("**I. Acquisition & Deployment (€)**")
            c1 = st.number_input("Software Licensing", value=150000, key="tco_c1", label_visibility="collapsed", help="Upfront software license costs")
            c2 = st.number_input("Migration & Integration", value=45000, key="tco_c2", label_visibility="collapsed", help="Cost of professional services for setup")
        with tco_cols[1]:
            st.markdown("**II. Annual Operational Costs (€)**")
            c3 = st.number_input("Cloud Infrastructure", value=60000, key="tco_c3", label_visibility="collapsed", help="Annual cost for servers, storage, etc.")
            c4 = st.number_input("Maintenance & Support", value=30000, key="tco_c4", label_visibility="collapsed", help="Annual support contract fee")
            c5 = st.number_input("Personnel", value=80000, key="tco_c5", label_visibility="collapsed", help="Annual cost for staff to manage the system")
        
        with tco_cols[2]:
            st.write("")
            st.write("")
            if st.button("Calculate TCO", key="tco_calc", use_container_width=True):
                total_tco = c1 + c2 + (5 * (c3 + c4 + c5))
                st.metric("5-Year Total Cost of Ownership", f"€ {total_tco:,.0f}")
                st.session_state.total_tco = total_tco

    with st.container(border=True):
        st.subheader("AI Commercial Model Recommendation")
        if 'total_tco' in st.session_state:
            st.success(f"Using calculated 5-Year TCO of **€{st.session_state.total_tco:,.0f}** for analysis.")
        
        segment = st.selectbox("Customer Segment", ["Tier 1 Operator", "Enterprise", "MVNO"])
        if st.button("Get AI Recommendation", key="tco_ai", use_container_width=True):
            if 'total_tco' in st.session_state:
                with st.spinner("AI is generating a strategic recommendation..."):
                    tco_components = f"Acquisition: €{c1+c2}, Annual Ops: €{c3+c4+c5}, 5-Year TCO: €{st.session_state.total_tco:,.0f}"
                    prompt = get_tco_pricing_prompt(segment, tco_components, "")
                    try:
                        message = client.messages.create(model="claude-3-sonnet-20240229", max_tokens=1024, messages=[{"role": "user", "content": prompt}]).content[0].text
                        recommendation = json.loads(message)
                        with st.expander("View AI Recommendation", expanded=True):
                            st.success(f"**Recommended Model:** {recommendation.get('recommended_model')}")
                            st.info(f"**TCO Insight:** {recommendation.get('tco_insight')}")
                            st.write("**Pricing Strategy:**"); st.write(recommendation.get('pricing_strategy'))
                            st.write("**Key Value Propositions:**")
                            for prop in recommendation.get('value_propositions', []): st.markdown(f"- {prop}")
                    except Exception as e:
                        st.error(f"AI Analysis Error: {e}")
            else:
                st.warning("Please calculate TCO first.")

def render_partner_page():
    st.markdown("### 🤝 Partner & Reseller Portal")
    with st.container(border=True):
        st.subheader("Performance Dashboard: *InnovateTel GmbH*")
        df_performance = db.get_partner_performance(partner_company_id=1)
        st.dataframe(df_performance, use_container_width=True, hide_index=True)

def render_rfx_page():
    st.markdown("### ⚙️ RFx Response Automation System")
    with st.container(border=True):
        st.subheader("Preliminary Risk Assessment: *FutureNet VoNR RFP*")
        df_rfx_risks = db.get_rfx_requirements(rfx_id=1)
        st.dataframe(df_rfx_risks, use_container_width=True, hide_index=True)

# --- MAIN APP LAYOUT & ROUTING ---
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

with st.sidebar:
    st.title("krmhstrk Assistant")
    st.write("Commercial Portfolio")
    st.markdown("---")
    
    page_options = {
        "Dashboard": "🏠", "Contract Lifecycle Management": "📄",
        "TCO & Pricing Optimization": "📊", "Partner & Reseller Portal": "🤝",
        "RFx Response Automation": "⚙️"
    }
    for page, icon in page_options.items():
        if st.button(f"{icon} {page}", use_container_width=True):
            st.session_state.page = page
            st.rerun()

setup_database()

page_function = {
    "Dashboard": render_main_dashboard, "Contract Lifecycle Management": render_contract_page,
    "TCO & Pricing Optimization": render_tco_page, "Partner & Reseller Portal": render_partner_page,
    "RFx Response Automation": render_rfx_page
}.get(st.session_state.page, render_main_dashboard)

page_function()
