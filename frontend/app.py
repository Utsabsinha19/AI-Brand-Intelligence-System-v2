import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime

import sys
import os
import tempfile
import sqlite3
import hashlib
import secrets

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

from backend.main_pipeline import run_pipeline

# Database Initialization
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password BLOB, salt BLOB, token TEXT)''')
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key, salt

def signup(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return False, "Username already exists."
    key, salt = hash_password(password)
    token = secrets.token_hex(16)
    c.execute("INSERT INTO users (username, password, salt, token) VALUES (?, ?, ?, ?)",
              (username, key, salt, token))
    conn.commit()
    conn.close()
    return True, "User created successfully. You can now log in."

def login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password, salt, token FROM users WHERE username=?", (username,))
    record = c.fetchone()
    conn.close()
    if record:
        stored_key, salt, token = record
        key, _ = hash_password(password, salt)
        if key == stored_key:
            return True, token
    return False, "Invalid username or password."

def generate_pdf_report(results):
    pdf = FPDF()
    pdf.add_page()
    
    # Title and Timestamp
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "AI Brand Intelligence Report", ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 10, f"Generated on: {now}", ln=True, align='C')
    pdf.ln(10)
    
    # AI Insight
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "AI Business Insight:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, results['insight'])
    pdf.ln(5)
    
    # Metrics
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Key Metrics:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"- Complaint Percentage: {results['complaint_percent']:.2f}%", ln=True)
    pdf.cell(0, 10, f"- Negative Sentiment: {results['negative_percent']:.2f}%", ln=True)
    pdf.cell(0, 10, f"- Total Records Analyzed: {len(results['dataframe'])}", ln=True)
    pdf.ln(5)
    
    # Keywords
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Top Keywords:", ln=True)
    pdf.set_font("Arial", '', 12)
    keywords_str = ", ".join(results['keywords'])
    pdf.multi_cell(0, 10, keywords_str)
    
    # Save to temp file and read bytes
    pdf.output("temp_report.pdf")
    with open("temp_report.pdf", "rb") as f:
        pdf_bytes = f.read()
    return pdf_bytes

if 'results' not in st.session_state:
    st.session_state['results'] = None
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'token' not in st.session_state:
    st.session_state['token'] = None

st.set_page_config(
    page_title="AI Brand Intelligence",
    layout="wide"
)

init_db()

# Authentication UI
if not st.session_state['logged_in']:
    st.title("🔒 AI Brand Intelligence - Login")
    st.markdown("Please sign in or create an account to access the dashboard.")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In"):
            success, token_or_msg = login(login_user, login_pass)
            if success:
                st.session_state['logged_in'] = True
                st.session_state['username'] = login_user
                st.session_state['token'] = token_or_msg
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(token_or_msg)
                
    with tab2:
        st.subheader("Sign Up")
        new_user = st.text_input("New Username", key="new_user")
        new_pass = st.text_input("New Password", type="password", key="new_pass")
        if st.button("Create Account"):
            if new_user and new_pass:
                success, msg = signup(new_user, new_pass)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Please enter both a username and a password.")
                
    st.stop() # Stops execution of the rest of the app until logged in

# Sidebar Profile & Logout
with st.sidebar:
    st.subheader("User Profile")
    st.write(f"**User:** {st.session_state['username']}")
    st.write(f"**Session Token:** `{st.session_state['token'][:8]}...`")
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['token'] = None
        st.session_state['results'] = None
        st.rerun()

st.title("AI Consumer Intelligence Dashboard")

st.markdown("""
### About This Project
The AI Brand Intelligence System processes consumer feedback, reviews, and comments to provide actionable business insights. 
Leveraging Natural Language Processing (NLP), this tool automatically helps you:
- 📊 **Analyze Sentiment:** Understand the overall mood of your customers.
- 🚨 **Detect Complaints:** Quickly flag critical customer service issues.
- 🔑 **Extract Keywords & Topics:** Discover the main subjects your customers are discussing.
- 💡 **Generate AI Insights:** Get automatic, high-level business recommendations based on the data.
""")

st.subheader("Input Consumer Data")

option = st.radio(
    "Choose Input Method",
    ["Upload CSV", "Paste Text"]
)

# =========================
# CSV Upload
# =========================

if option == "Upload CSV":

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file:

        if st.button("Analyze CSV"):
            with st.spinner("Analyzing consumer data... This may take a moment."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                        tmp.write(uploaded_file.getbuffer())
                        tmp_path = tmp.name
                    
                    st.session_state['results'] = run_pipeline(tmp_path)
                    os.remove(tmp_path)
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")

# =========================
# Manual Text Input
# =========================

elif option == "Paste Text":

    st.info(
        "Enter one customer review/comment per line."
    )

    user_text = st.text_area(
        "",
        height=300,
        placeholder="Type or paste customer feedback here..."
    )

    if st.button("Analyze Text"):

        if user_text.strip() != "":

            lines = user_text.split("\n")

            posts = [
                line.strip()
                for line in lines
                if line.strip() != ""
            ]

            import pandas as pd

            df = pd.DataFrame({
                "text": posts
            })

            with st.spinner("Processing text feedback..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                        df.to_csv(tmp.name, index=False)
                        tmp_path = tmp.name

                    st.session_state['results'] = run_pipeline(tmp_path)
                    os.remove(tmp_path)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if st.session_state['results'] is not None:

    results = st.session_state['results']
    df = results['dataframe']
    
    # Create elegant UI tabs for enterprise feel
    tab1, tab2, tab3 = st.tabs(["📊 Analytics overview", "🗂️ Data explorer", "🔑 Topics & keywords"])

    with tab1:
        st.subheader("Key insights & AI analysis")
        
        # Professional Insight Box using st.info with material icon
        st.info(results['insight'], icon=":material/lightbulb:")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total records", len(df))
        with col2:
            st.metric("Complaint rate", f"{results['complaint_percent']:.1f}%")
        with col3:
            st.metric("Negative sentiment", f"{results['negative_percent']:.1f}%")
        with col4:
            st.metric("Topics extracted", len(results['topics']))
            
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.subheader("Sentiment distribution")
            sentiment_counts = df['sentiment'].str.title().value_counts()
            fig_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig_pie)
            
        with chart_col2:
            st.subheader("Brand health dimensions")
            sentiment_pcts = df['sentiment'].str.title().value_counts(normalize=True) * 100
            pos_pct = sentiment_pcts.get('Positive', 0)
            neu_pct = sentiment_pcts.get('Neutral', 0)
            
            radar_df = pd.DataFrame({
                'Dimension': ['Positive sentiment', 'Neutral sentiment', 'Negative sentiment', 'Complaint rate'],
                'Score': [pos_pct, neu_pct, results['negative_percent'], results['complaint_percent']]
            })
            
            fig_radar = px.line_polar(
                radar_df,
                r='Score',
                theta='Dimension',
                line_close=True,
                color_discrete_sequence=['#4361EE']
            )
            fig_radar.update_traces(fill='toself')
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
                    angularaxis=dict(tickfont=dict(size=12))
                ),
                margin=dict(t=10, b=10, l=30, r=30)
            )
            st.plotly_chart(fig_radar)

        st.subheader("Key drivers & highlighted factors")
        if len(results['keywords']) > 0:
            top_keywords = results['keywords'][:8]
            badges_html = " ".join([f":blue-badge[{kw.title()}]" for kw in top_keywords])
            st.markdown(f"**Trending terms driving sentiment:** {badges_html}")
            
        if len(results['topics']) > 0:
            st.markdown("**Core conversational themes:**")
            for topic in results['topics'][:3]:
                st.caption(f"• {topic}")

    with tab2:
        st.subheader("Processed consumer data")
        st.dataframe(df)

    with tab3:
        st.subheader("Detected topics")
        for topic in results['topics']:
            st.info(topic, icon=":material/forum:")

        st.subheader("Top keywords")
        badges_html_all = " ".join([f":blue-badge[{kw.title()}]" for kw in results['keywords']])
        st.markdown(badges_html_all)

        keywords_text = "\n".join(results['keywords'])
        st.download_button(
            label="Download keywords as TXT",
            data=keywords_text,
            file_name="extracted_keywords.txt",
            mime="text/plain"
        )

    # =========================
    # Export & Actions
    # =========================

    st.subheader("Export & actions")
    
    col_x, col_y, col_z = st.columns(3)
    
    with col_x:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download processed CSV",
            data=csv_data,
            file_name="processed_insights.csv",
            mime="text/csv"
        )
        
    with col_y:
        pdf_report = generate_pdf_report(results)
        st.download_button(
            label="📄 Download PDF report",
            data=pdf_report,
            file_name="brand_intelligence_report.pdf",
            mime="application/pdf"
        )
        
    with col_z:
        if st.button("🗑️ Clear data"):
            st.session_state['results'] = None
            st.rerun()