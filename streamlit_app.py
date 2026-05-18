import streamlit as st
import pandas as pd
import numpy as np
from transformers import pipeline

# --- Pipeline & Categories Definition ---

@st.cache_resource
def load_pipeline():
    """Loads the Zero-Shot Classification pipeline and caches it."""
    # You can use other models like 'valhalla/distilbart-mnli-12-3' for a smaller/faster option
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

classifier = load_pipeline()
 
# 1. Page Configuration
st.set_page_config(
    page_title="Brand Intelligence Analytics",
    page_icon="📊",
    layout="wide"
)

# 2. Header
st.title("Brand Intelligence Real-Time Node")
st.markdown("""
**Tech Stack:** Python 3.10+ | Transformers | FastAPI | PostgreSQL | Redis | Streamlit
""")

# Define the categories you want to classify the text into.
CANDIDATE_LABELS = [
    "Product Feedback", "Complaint", "Customer Support", 
    "Pricing Inquiry", "Feature Request", "Positive Mention", "Spam/Irrelevant"
]

# 3. Initialize Session State for our live feed
if "mentions" not in st.session_state:
    st.session_state.mentions = pd.DataFrame(columns=["Mention", "Category", "Score", "Decision"])

# 4. Sidebar - Input & Bulk Upload
with st.sidebar:
    st.header("Analyze Mentions")
    
    # Single text input
    mention_input = st.text_area("Paste a brand mention here...")
    if st.button("Analyze Text", type="primary"):
        if mention_input:
            with st.spinner("Analyzing text..."):
                # --- Zero-Shot Classification Logic ---
                # The pipeline takes the text and the candidate labels
                # multi_label=False ensures scores sum to 1 (like a softmax)
                result = classifier(mention_input, CANDIDATE_LABELS, multi_label=False)
                
                # The result is a dictionary with 'labels' and 'scores'
                top_category = result['labels'][0]
                top_score = round(result['scores'][0], 2)

                # A score > 0.5 indicates a reasonably confident classification
                decision = "Keep" if top_score > 0.5 else "Review"
                
                new_data = pd.DataFrame({
                    "Mention": [mention_input],
                    "Category": [top_category],
                    "Score": [top_score],
                    "Decision": [decision]
                })
                # Append new analysis to the top of our session state dataframe
                st.session_state.mentions = pd.concat([new_data, st.session_state.mentions], ignore_index=True)
            st.success("Analysis complete!")
        else:
            st.warning("Please enter some text to analyze.")
            
    st.divider()
    
    # Bulk File Upload
    st.header("Bulk Upload")
    uploaded_file = st.file_uploader("Upload dataset (CSV/TXT)", type=['csv', 'txt'])
    if uploaded_file is not None:
        if st.button("Process Uploaded File"):
            with st.spinner(f"Processing {uploaded_file.name}..."):
                try:
                    # Determine file type and read mentions
                    if uploaded_file.type == "text/csv":
                        df = pd.read_csv(uploaded_file)
                        if 'text' not in df.columns:
                            st.error("Uploaded CSV must contain a 'text' column.")
                            st.stop() # Stop execution if column is missing
                        mentions_to_process = df['text'].dropna().tolist()
                    else: # text/plain
                        mentions_to_process = [line.decode("utf-8").strip() for line in uploaded_file.readlines() if line.strip()]

                    if not mentions_to_process:
                        st.warning("No text found in the uploaded file.")
                    else:
                        # The pipeline can process a list of sequences for efficiency
                        bulk_results = classifier(mentions_to_process, CANDIDATE_LABELS, multi_label=False)
                        
                        # The output is a list of dictionaries, one for each input text.
                        # We extract the top label and score for each.
                        top_categories = [result['labels'][0] for result in bulk_results]
                        top_scores = [round(result['scores'][0], 2) for result in bulk_results]
                        
                        # Create a DataFrame with the results
                        results_df = pd.DataFrame({
                            "Mention": mentions_to_process,
                            "Category": top_categories,
                            "Score": top_scores,
                        })
                        results_df["Decision"] = results_df["Score"].apply(lambda s: "Keep" if s > 0.5 else "Review")
                        
                        # Prepend the new results to the main dataframe
                        st.session_state.mentions = pd.concat([results_df, st.session_state.mentions], ignore_index=True)
                        st.success(f"Successfully processed {len(mentions_to_process)} mentions from {uploaded_file.name}!")
                except Exception as e:
                    st.error(f"Error processing file: {e}")

# 5. Dashboard Metrics
st.subheader("Live Analytics")
col1, col2, col3 = st.columns(3)

total_count = len(st.session_state.mentions)
avg_confidence = st.session_state.mentions["Score"].mean() if total_count > 0 else 0.0
highest_category = st.session_state.mentions["Category"].mode()[0] if total_count > 0 else "-"

col1.metric(label="Mentions Analyzed", value=f"{total_count}")
col2.metric(label="Avg. Confidence", value=f"{avg_confidence:.2f}")
col3.metric(label="Highest Category", value=highest_category)

st.divider()

# 6. Layout for Charts and Feed
st.subheader("Visualizations")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("##### Confidence Trend")
    if total_count > 1:
        st.line_chart(st.session_state.mentions["Score"][::-1].reset_index(drop=True))
    else:
        # Placeholder chart until we get more data
        placeholder_data = pd.DataFrame(np.random.randn(20, 1) * 0.1 + 0.8, columns=['Score'])
        st.line_chart(placeholder_data)

with chart_col2:
    st.markdown("##### Category Distribution")
    if total_count > 0:
        category_dist = st.session_state.mentions['Category'].value_counts()
        st.bar_chart(category_dist, use_container_width=True)
    else:
        st.text("Awaiting data for category analysis...")

st.subheader("Real-Time Mentions Stream")
if total_count > 0:
    st.dataframe(st.session_state.mentions, use_container_width=True, height=350)
else:
    st.info("No mentions analyzed yet. Paste text or upload a file in the sidebar to begin.")