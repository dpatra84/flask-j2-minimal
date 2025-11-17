from flask import Flask
from app.config import Config
from flask_migrate import Migrate
from app.models import login_manager, db



app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "login"  # The route for the login page

migrate = Migrate()
migrate.init_app(app, db)


from app import routes
from app.routes import auth, llm
