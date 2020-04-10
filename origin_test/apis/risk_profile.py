from flask_restplus import Namespace, Resource

from origin_test.schemas.risk_api import RiskProfileCalculationSchema
from origin_test.utils.validations import check_body

risk_profile_ns = Namespace("risk_profile")


@risk_profile_ns.route("/")
class RiskProfileResource(Resource):
    @check_body(RiskProfileCalculationSchema)
    def post(self):
        return {"message": "I\'m Healthy"}
