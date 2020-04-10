from marshmallow import fields

from origin_test.schemas.house import HouseSchema
from origin_test.schemas.user import UserSchema
from origin_test.schemas.vehicle import VehicleSchema


class RiskProfileCalculationSchema(UserSchema):
    """
    Risk Profile heritages from UserSchema because the payload root has all fields from it. If you change UserSchema,
    it will change this schema too.
    """
    house = fields.Nested(HouseSchema)
    vehicle = fields.Nested(VehicleSchema)
