import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ['PGHOST'],
            database=os.environ['PGDATABASE'],
            user=os.environ['PGUSER'],
            password=os.environ['PGPASSWORD'],
            port=os.environ['PGPORT']
        )
        self._create_tables()

    def _create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS income (
                    id SERIAL PRIMARY KEY,
                    amount DECIMAL(10,2) NOT NULL,
                    source VARCHAR(50) NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    is_recurring BOOLEAN DEFAULT FALSE,
                    frequency VARCHAR(20),
                    next_due_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS tithe_payments (
                    id SERIAL PRIMARY KEY,
                    amount DECIMAL(10,2) NOT NULL,
                    payment_date DATE NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()

    def add_income(self, amount, source, description, is_recurring=False, frequency=None):
        with self.conn.cursor() as cur:
            next_due_date = None
            if is_recurring and frequency:
                today = datetime.now().date()
                if frequency == 'Weekly':
                    next_due_date = today + timedelta(days=7)
                elif frequency == 'Monthly':
                    next_due_date = today + timedelta(days=30)
                elif frequency == 'Yearly':
                    next_due_date = today + timedelta(days=365)
            
            cur.execute(
                """INSERT INTO income 
                   (amount, source, description, date, is_recurring, frequency, next_due_date) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (amount, source, description, datetime.now().date(), 
                 is_recurring, frequency, next_due_date)
            )
            self.conn.commit()
            
    def get_recurring_income(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM income 
                WHERE is_recurring = TRUE 
                ORDER BY next_due_date ASC
            """)
            return cur.fetchall()

    def add_tithe_payment(self, amount, notes):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tithe_payments (amount, payment_date, notes) VALUES (%s, %s, %s)",
                (amount, datetime.now().date(), notes)
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
                SELECT amount, source, date, description
                FROM income
                ORDER BY date DESC
                LIMIT %s
            """, (limit,))
            return cur.fetchall()

    def get_tithe_status(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                WITH total_income AS (
                    SELECT COALESCE(SUM(amount), 0) as income_sum
                    FROM income
                ),
                total_payments AS (
                    SELECT COALESCE(SUM(amount), 0) as payment_sum
                    FROM tithe_payments
                )
                SELECT 
                    (total_income.income_sum * 0.1) as total_tithe_due,
                    total_payments.payment_sum as total_tithe_paid,
                    ((total_income.income_sum * 0.9) - total_payments.payment_sum) as remaining_balance
                FROM total_income, total_payments
            """)
            return cur.fetchone()
