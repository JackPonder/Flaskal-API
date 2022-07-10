import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"
    CORS_HEADERS = 'Content-Type'
    TEMPLATES_FOLDER = "templates"
    STATIC_FOLDER = "static"


class DevConfig(Config):
    FLASK_ENV = "development"
    TESTING = False
    DEBUG = True


class ProdConfig(Config):
    FLASK_ENV = "production"
    TESTING = False
    DEBUG = False


config = {
    "development": DevConfig,
    "production": ProdConfig,
}
