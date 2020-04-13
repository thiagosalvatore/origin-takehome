from flask import Blueprint

from origin_takehome.apis.health_check import health_check_ns
from origin_takehome.apis.risk_profile import risk_profile_ns
from origin_takehome.utils.api import CustomAPI

origin_test_bp = Blueprint("origin_test_api", __name__)

api = CustomAPI(origin_test_bp, decorators=[])

api.add_namespace(health_check_ns)
api.add_namespace(risk_profile_ns)
