import bcrypt
import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database import Database

# Generate a secret key for JWT
SECRET_KEY = os.urandom(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

def get_password_hash(password: str) -> str:
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), 
                         hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    """Create a new access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify an access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

class AuthManager:
    def __init__(self, db: Database):
        self.db = db

    def register_user(self, email: str, password: str, name: str) -> dict:
        """Register a new user"""
        with self.db.conn.cursor() as cur:
            # Check if user exists
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cur.fetchone() is not None:
                return None

            # Create new user
            password_hash = get_password_hash(password)
            cur.execute(
                """INSERT INTO users (email, password_hash, name)
                   VALUES (%s, %s, %s) RETURNING id, email, name""",
                (email, password_hash, name)
            )
            user = cur.fetchone()
            self.db.conn.commit()
            return {
                "id": user[0],
                "email": user[1],
                "name": user[2]
            }

    def authenticate_user(self, email: str, password: str) -> dict:
        """Authenticate a user"""
        with self.db.conn.cursor() as cur:
            cur.execute(
                """SELECT id, email, name, password_hash
                   FROM users WHERE email = %s""",
                (email,)
            )
            user = cur.fetchone()
            
            if user is None:
                return None
            
            if not verify_password(password, user[3]):
                return None

            return {
                "id": user[0],
                "email": user[1],
                "name": user[2]
            }

    def get_user_by_id(self, user_id: int) -> dict:
        """Get user by ID"""
        with self.db.conn.cursor() as cur:
            cur.execute(
                """SELECT id, email, name FROM users WHERE id = %s""",
                (user_id,)
            )
            user = cur.fetchone()
            if user is None:
                return None
            return {
                "id": user[0],
                "email": user[1],
                "name": user[2]
            }

    def update_user_profile(self, user_id: int, name: str = None, email: str = None, password: str = None) -> dict:
        """Update user profile information"""
        updates = []
        values = []
        if name:
            updates.append("name = %s")
            values.append(name)
        if email:
            updates.append("email = %s")
            values.append(email)
        if password:
            updates.append("password_hash = %s")
            values.append(get_password_hash(password))
        
        if not updates:
            return None

        with self.db.conn.cursor() as cur:
            query = f"""
                UPDATE users 
                SET {', '.join(updates)}
                WHERE id = %s
                RETURNING id, email, name
            """
            values.append(user_id)
            cur.execute(query, values)
            user = cur.fetchone()
            self.db.conn.commit()
            
            if user is None:
                return None
            return {
                "id": user[0],
                "email": user[1],
                "name": user[2]
            }
