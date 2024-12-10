import streamlit as st
import pandas as pd
from database import Database
from utils import format_currency, calculate_tithe, validate_amount, INCOME_SOURCES, get_sacred_geometry_style
from visualizations import create_income_distribution_chart, create_tithe_progress_chart
from styles import apply_custom_styles

# Initialize database
db = Database()

# Page config
st.set_page_config(
    page_title="Sacred Tithe Tracker",
    page_icon="🙏",
    layout="wide"
)

# Apply custom styles
st.markdown(apply_custom_styles(), unsafe_allow_html=True)
st.markdown(get_sacred_geometry_style(), unsafe_allow_html=True)

# Header
st.title("🙏 Sacred Tithe Tracker")
st.markdown("*'Bring the whole tithe into the storehouse...' - Malachi 3:10*")

# Sidebar for data entry
with st.sidebar:
    st.markdown("### Record New Income")
    amount = st.number_input("Amount", min_value=0.0, format="%f")
    source = st.selectbox("Source", INCOME_SOURCES)
    description = st.text_area("Description")
    
    if st.button("Record Income"):
        if amount > 0:
            db.add_income(amount, source, description)
            st.success("Income recorded successfully!")
        else:
            st.error("Please enter a valid amount")
    
    st.markdown("---")
    
    st.markdown("### Record Tithe Payment")
    tithe_amount = st.number_input("Tithe Amount", min_value=0.0, format="%f")
    notes = st.text_area("Payment Notes")
    
    if st.button("Record Tithe Payment"):
        if tithe_amount > 0:
            db.add_tithe_payment(tithe_amount, notes)
            st.success("Tithe payment recorded successfully!")
        else:
            st.error("Please enter a valid amount")

# Main content
col1, col2, col3 = st.columns(3)

# Fetch tithe status
tithe_status = db.get_tithe_status()
total_tithe_due = float(tithe_status['total_tithe_due'])
total_tithe_paid = float(tithe_status['total_tithe_paid'])

# Display metrics
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total Tithe Due</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{format_currency(total_tithe_due)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total Tithe Paid</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{format_currency(total_tithe_paid)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Remaining Balance</div>', unsafe_allow_html=True)
    remaining_balance = float(tithe_status['remaining_balance'])
    st.markdown(f'<div class="metric-value">{format_currency(remaining_balance)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Visualizations
st.markdown("### Income Distribution")
income_summary = db.get_income_summary()
if income_summary:
    chart = create_income_distribution_chart(income_summary)
    st.plotly_chart(chart, use_container_width=True)

st.markdown("### Tithe Progress")
progress_chart = create_tithe_progress_chart(total_tithe_due, total_tithe_paid)
st.plotly_chart(progress_chart, use_container_width=True)

# Recent transactions
st.markdown("### Recent Transactions")
transactions = db.get_recent_transactions()
if transactions:
    df = pd.DataFrame(transactions)
    df['amount'] = df['amount'].apply(format_currency)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No transactions recorded yet.")
