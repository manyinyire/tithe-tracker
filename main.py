import streamlit as st
import pandas as pd
from datetime import datetime
from database import Database
from auth import AuthManager
from utils import format_currency, calculate_tithe, validate_amount, INCOME_SOURCES, get_sacred_geometry_style, TITHE_VERSES
import random
from visualizations import create_income_distribution_chart, create_tithe_progress_chart
from styles import apply_custom_styles

# Initialize database and auth
db = Database()
auth_manager = AuthManager(db)

# Page config
st.set_page_config(
    page_title="Sacred Tithe Tracker",
    page_icon="🙏",
    layout="wide"
)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'authentication_status' not in st.session_state:
    st.session_state.authentication_status = None

def login_page():
    st.title("🙏 Welcome to Sacred Tithe Tracker")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if email and password:
                user = auth_manager.authenticate_user(email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.authentication_status = True
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.error("Please fill in all fields")
    
    with tab2:
        name = st.text_input("Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        
        if st.button("Sign Up"):
            if name and email and password:
                user = auth_manager.register_user(email, password, name)
                if user:
                    st.success("Account created successfully! Please login.")
                    st.rerun()
                else:
                    st.error("Email already registered")
            else:
                st.error("Please fill in all fields")

# Apply custom styles
st.markdown(apply_custom_styles(), unsafe_allow_html=True)
st.markdown(get_sacred_geometry_style(), unsafe_allow_html=True)

# Show login page if user is not logged in
if not st.session_state.authentication_status:
    login_page()
elif st.session_state.user is not None:
    # Header with logout button
    col1, col2 = st.columns([6,1])
    with col1:
        st.title("🙏 Sacred Tithe Tracker")
        st.markdown("*'Bring the whole tithe into the storehouse...' - Malachi 3:10*")
    with col2:
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.authentication_status = None
            st.rerun()

    # Sidebar for data entry
    with st.sidebar:
        st.markdown("### Record New Income")
        amount = st.number_input("Amount", min_value=0.0, format="%f")
        source = st.selectbox("Source", INCOME_SOURCES)
        description = st.text_area("Description")
    
    # Recurring income options
    is_recurring = st.checkbox("Is this a recurring income?")
    frequency = None
    if is_recurring:
        frequency = st.selectbox(
            "Frequency",
            ["Weekly", "Monthly", "Yearly"]
        )
    
    if st.button("Record Income"):
        if amount > 0:
            db.add_income(st.session_state.user["id"], amount, source, description, is_recurring, frequency)
            st.success("Income recorded successfully!")
        else:
            st.error("Please enter a valid amount")
    
    st.markdown("---")
    
    st.markdown("### Record Tithe Payment")
    tithe_amount = st.number_input("Tithe Amount", min_value=0.0, format="%f")
    notes = st.text_area("Payment Notes")
    
    if st.button("Record Tithe Payment"):
        if tithe_amount > 0:
            db.add_tithe_payment(st.session_state.user["id"], tithe_amount, notes)
            verse = random.choice(TITHE_VERSES)
            st.success(f"🙏 Tithe payment recorded successfully! May God bless your faithful giving.\n\n*{verse}*")
        else:
            st.error("Please enter a valid amount")

# Main content area - only show when user is logged in
    if st.session_state.authentication_status and st.session_state.user:
        col1, col2, col3 = st.columns(3)

        # Fetch tithe status
        try:
            tithe_status = db.get_tithe_status(st.session_state.user["id"])
            if tithe_status:
                total_tithe_due = float(tithe_status['total_tithe_due'])
                total_tithe_paid = float(tithe_status['total_tithe_paid'])
            else:
                total_tithe_due = 0.0
                total_tithe_paid = 0.0
        except Exception as e:
            st.error(f"Error fetching tithe status: {str(e)}")
            total_tithe_due = 0.0
            total_tithe_paid = 0.0

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
        income_summary = db.get_income_summary(st.session_state.user["id"])
        if income_summary:
            chart = create_income_distribution_chart(income_summary)
            st.plotly_chart(chart, use_container_width=True)

        st.markdown("### Tithe Progress")
        progress_chart = create_tithe_progress_chart(total_tithe_due, total_tithe_paid)
        st.plotly_chart(progress_chart, use_container_width=True)

        # Recurring Income Section
        st.markdown("### 🔄 Recurring Income")
        recurring_incomes = db.get_recurring_income()
        if recurring_incomes:
            for income in recurring_incomes:
                with st.expander(f"{income['source']} - {format_currency(income['amount'])} ({income['frequency']})"):
                    st.write(f"**Description:** {income['description']}")
                    st.write(f"**Next Due:** {income['next_due_date'].strftime('%Y-%m-%d')}")
                    st.write(f"**Frequency:** {income['frequency']}")
                    days_until_due = (income['next_due_date'] - datetime.now().date()).days
                    if days_until_due <= 7:
                        st.warning(f"⚠️ Due in {days_until_due} days!")
                    else:
                        st.info(f"Next payment in {days_until_due} days")
        else:
            st.info("No recurring income set up yet.")

        # Recent transactions
        st.markdown("### Recent Transactions")
        transactions = db.get_recent_transactions(st.session_state.user["id"])
        if transactions:
            df = pd.DataFrame(transactions)
            df['amount'] = df['amount'].apply(format_currency)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No transactions recorded yet.")
