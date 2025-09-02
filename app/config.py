import os
import secrets

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))
JWT_EMAIL_ACTIVATION_EXPIRE_MINUTES = int(
    os.getenv("JWT_EMAIL_ACTIVATION_EXPIRE_MINUTES", 60)
)

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GMAIL_SMTP_HOST = os.getenv("GMAIL_SMTP_HOST")
GMAIL_SMTP_PORT = os.getenv("GMAIL_SMTP_PORT")
