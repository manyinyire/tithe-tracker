import os
from datetime import datetime
from psycopg2.extras import RealDictCursor
import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'])
        with self.conn.cursor() as cur:
            # Create income table with currency support
            cur.execute("""
                CREATE TABLE IF NOT EXISTS income (
                    id SERIAL PRIMARY KEY,
                    amount DECIMAL(15, 2) NOT NULL,
                    source VARCHAR(255) NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    currency VARCHAR(3) DEFAULT 'USD'
                );
            """)
            
            # Create tithe_payments table with currency support
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tithe_payments (
                    id SERIAL PRIMARY KEY,
                    amount DECIMAL(15, 2) NOT NULL,
                    payment_date DATE NOT NULL,
                    notes TEXT,
                    currency VARCHAR(3) DEFAULT 'USD'
                );
            """)
            
            # Create exchange_rates table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS exchange_rates (
                    id SERIAL PRIMARY KEY,
                    currency_code VARCHAR(3) NOT NULL,
                    date DATE NOT NULL,
                    rate DECIMAL(10, 4) NOT NULL,
                    UNIQUE(currency_code, date)
                );
            """)
            
            # Create supported_currencies table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS supported_currencies (
                    code VARCHAR(3) PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    symbol VARCHAR(5) NOT NULL
                );
            """)
            self.conn.commit()

    def get_exchange_rate(self, currency_code, date=None):
        if currency_code == 'USD':
            return 1.0
        
        if date is None:
            date = datetime.now().date()
            
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT rate FROM exchange_rates WHERE currency_code = %s AND date = %s",
                (currency_code, date)
            )
            result = cur.fetchone()
            return float(result[0]) if result else None

    def convert_to_usd(self, amount, currency_code, date=None):
        if currency_code == 'USD':
            return amount
        
        rate = self.get_exchange_rate(currency_code, date)
        if rate is None:
            raise ValueError(f"No exchange rate found for {currency_code}")
        
        return amount * rate

    def get_supported_currencies(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT code, name, symbol FROM supported_currencies ORDER BY code")
            return cur.fetchall()

    def add_income(self, amount, source, description, currency='USD'):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO income (amount, source, description, date, currency) VALUES (%s, %s, %s, %s, %s)",
                (amount, source, description, datetime.now().date(), currency)
            )
            self.conn.commit()

    def add_tithe_payment(self, amount, notes, currency='USD'):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tithe_payments (amount, payment_date, notes, currency) VALUES (%s, %s, %s, %s)",
                (amount, datetime.now().date(), notes, currency)
            )
            self.conn.commit()

    def get_income_summary(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT source, SUM(amount) as total
                FROM income
                GROUP BY source
                ORDER BY total DESC
            """)
            return cur.fetchall()

    def get_recent_transactions(self, limit=10):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT amount, source, date, description, currency
                FROM income
                ORDER BY date DESC
                LIMIT %s
            """, (limit,))
            return cur.fetchall()

    def get_tithe_status(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                WITH converted_income AS (
                    SELECT 
                        amount * COALESCE(e.rate, 1) as usd_amount
                    FROM income i
                    LEFT JOIN exchange_rates e ON i.currency = e.currency_code 
                        AND i.date = e.date
                    WHERE i.currency != 'USD'
                    UNION ALL
                    SELECT amount as usd_amount
                    FROM income 
                    WHERE currency = 'USD'
                ),
                converted_payments AS (
                    SELECT 
                        amount * COALESCE(e.rate, 1) as usd_amount
                    FROM tithe_payments t
                    LEFT JOIN exchange_rates e ON t.currency = e.currency_code 
                        AND t.payment_date = e.date
                    WHERE t.currency != 'USD'
                    UNION ALL
                    SELECT amount as usd_amount
                    FROM tithe_payments 
                    WHERE currency = 'USD'
                )
                SELECT 
                    (COALESCE(SUM(i.usd_amount), 0) * 0.1) as total_tithe_due,
                    COALESCE(SUM(p.usd_amount), 0) as total_tithe_paid,
                    (COALESCE(SUM(i.usd_amount), 0) * 0.1 - COALESCE(SUM(p.usd_amount), 0)) as remaining_balance
                FROM 
                    (SELECT COALESCE(SUM(usd_amount), 0) as usd_amount FROM converted_income) i,
                    (SELECT COALESCE(SUM(usd_amount), 0) as usd_amount FROM converted_payments) p
            """)
            return cur.fetchone()
