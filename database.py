import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

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

    def add_income(self, amount, source, description):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO income (amount, source, description, date) VALUES (%s, %s, %s, %s)",
                (amount, source, description, datetime.now().date())
            )
            self.conn.commit()

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
                SELECT 
                    COALESCE(SUM(i.amount) * 0.1, 0) as total_tithe_due,
                    COALESCE(SUM(tp.amount), 0) as total_tithe_paid
                FROM income i
                LEFT JOIN tithe_payments tp ON true
            """)
            return cur.fetchone()
