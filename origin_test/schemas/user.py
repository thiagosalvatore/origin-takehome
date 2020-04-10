from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    age = fields.Integer(required=True, validate=validate.Range(min=0, error="Age must be greater than 0"))
    dependents = fields.Integer(required=True, validate=validate.Range(min=0,
                                                                       error="Dependents must be greater than 0"))
    income = fields.Integer(required=True, validate=validate.Range(min=0,
                                                                   error="Income must be greater than 0"))
    marital_status = fields.String(required=True, validate=validate.OneOf(["single", "married"]))
    risk_questions = fields.List(fields.Integer, required=True, validate=validate.Length(3))
