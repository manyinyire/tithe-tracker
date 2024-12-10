import streamlit as st
from datetime import datetime

def format_currency(amount):
    return f"${amount:,.2f}"

def calculate_tithe(amount):
    return amount * 0.1

def validate_amount(amount):
    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be greater than zero"
        return True, amount
    except ValueError:
        return False, "Please enter a valid number"

INCOME_SOURCES = [
    "Salary",
    "Business Income",
    "Side Hustle",
    "Gifts",
    "Investments",
    "Other"
]

def get_sacred_geometry_style():
    return """
        <style>
        .stApp {
            background: linear-gradient(135deg, #f6f5f7 0%, #ffffff 100%);
        }
        .css-1d391kg {
            background: linear-gradient(to right, #6B46C1 0%, #805AD5 100%);
        }
        .stButton>button {
            background: linear-gradient(45deg, #6B46C1 0%, #805AD5 100%);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 0.5rem 2rem;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #6B46C1;
        }
        </style>
    """
