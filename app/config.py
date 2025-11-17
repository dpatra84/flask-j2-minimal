import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    """Base configuration (sane defaults for production)."""

    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    APP_NAME = os.getenv("APP_NAME", "Flask J2 Minimal")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    APP_AUTHOR = os.getenv("APP_AUTHOR", "shivishbrahma")

    PORT = int(os.getenv("PORT", 5000))
    ENV = os.getenv("APP_ENV", "development")
    DEBUG = ENV == "development"
    TESTING = False

    # Use an absolute path for the database file
    APP_PATH = os.path.abspath(
        os.path.dirname(os.path.dirname(__file__))
    )  # Go up one level to 'flask-j2-minimal'
    UPLOAD_FOLDER = os.path.join(APP_PATH, "storage/uploads")
    ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

    # Server / sessions
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = timedelta(days=int(os.getenv("REMEMBER_DAYS", "7")))

    # Database (SQLAlchemy)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///" + os.path.join(APP_PATH, "storage/app.sqlite3")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False") == "True"
