import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

class DevConfig(Config):
    DEBUG = True
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

class ProdConfig(Config):
    DEBUG = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
