from app import app
from datetime import datetime
from flask import render_template

@app.context_processor
def inject_config_vars():
    return dict(
        app_name=app.config["APP_NAME"],
        version=app.config["APP_VERSION"],
        author=app.config["APP_AUTHOR"],
        year=datetime.now().year
    )


@app.route("/")
def index():
    # If models are used, import and use here
    return render_template("index.j2", name="World")
