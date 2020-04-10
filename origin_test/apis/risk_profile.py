from flask_restplus import Namespace, Resource

from origin_test.schemas.risk_api import RiskProfileCalculationSchema, RiskProfileSchema
from origin_test.services.risk_profile import RiskProfileService
from origin_test.utils.validations import check_body

risk_profile_ns = Namespace("risk_profile")


@risk_profile_ns.route("/")
class RiskProfileResource(Resource):
    @check_body(RiskProfileCalculationSchema)
    def post(self, data):
        profile_risk = RiskProfileService(data).calculate_risk_profile()
        return RiskProfileSchema().dump(profile_risk)
