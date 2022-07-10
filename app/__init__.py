from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
from .config import config

mail = Mail()
migrate = Migrate(compare_type=True)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "views.login"
login_manager.login_message = None


def create_app(config_type="development"):
    app = Flask(__name__)
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.config.from_object(config[config_type])

    from .views import views
    app.register_blueprint(views)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    mail.init_app(app)
    CORS(app)

    return app
