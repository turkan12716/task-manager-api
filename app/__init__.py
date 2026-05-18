import os
from flask import Flask
from .routes import bp

def create_app():
    app = Flask(__name__)
    
    # Externalized configuration via environment variables
    app.config["APP_VERSION"] = os.getenv("APP_VERSION", "1.0.0")
    app.config["MAX_TASKS"] = int(os.getenv("MAX_TASKS", "100"))
    
    # In-memory data structures
    app.config['TASKS'] = []
    app.config['TASK_COUNTER'] = 0

    app.register_blueprint(bp)
    return app
