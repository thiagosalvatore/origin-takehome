from marshmallow import Schema, fields


class VehicleSchema(Schema):
    year = fields.Integer(required=True)
