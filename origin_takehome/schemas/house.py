from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class HouseSchema(Schema):
    ownership_status = fields.String(required=True, validate=OneOf(["owned", "mortgaged"]))
