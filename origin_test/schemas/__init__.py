from bson import ObjectId
from marshmallow import Schema, fields

Schema.TYPE_MAPPING[ObjectId] = fields.String
