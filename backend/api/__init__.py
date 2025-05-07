from flask import Blueprint
from backend.api.events_api import events_api

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Register routes
api_bp.register_blueprint(events_api)
