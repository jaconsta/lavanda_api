from marshmallow_mongoengine import ModelSchema
from marshmallow import fields

from ..models.User import User, LaundrymanDataEmbedded


class LaundrymanDataSchema(ModelSchema):
    approved = fields.Boolean(default=False, read_only=True)

    class Meta:
        model = LaundrymanDataEmbedded


class RegisterSchema(ModelSchema):
    class Meta:
        model = User
