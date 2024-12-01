from flask import Flask
from .routes import production_plan_api

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/productionplan', 'productionplan', production_plan_api, methods=["POST"])
    return app