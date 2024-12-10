import streamlit as st

def format_currency(amount, currency='USD'):
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£'
    }
    symbol = symbols.get(currency, '$')
    return f"{symbol}{amount:,.2f}"

def calculate_tithe(amount):
    return amount * 0.1

def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, "Amount must be greater than 0"
        return True, amount
    except ValueError:
        return False, "Please enter a valid number"

TITHE_VERSES = [
    "Bring the whole tithe into the storehouse, that there may be food in my house. Test me in this, says the LORD Almighty. - Malachi 3:10",
    "Give, and it will be given to you. - Luke 6:38",
    "Each of you should give what you have decided in your heart to give, not reluctantly or under compulsion, for God loves a cheerful giver. - 2 Corinthians 9:7",
    "Honor the LORD with your wealth, with the firstfruits of all your crops. - Proverbs 3:9",
    "But who am I, and who are my people, that we should be able to give as generously as this? Everything comes from you, and we have given you only what comes from your hand. - 1 Chronicles 29:14"
]

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
