from marshmallow_mongoengine import ModelSchema

from .models import OrderInformation, UserRequestEmbedded


class OrderInformationSchema(ModelSchema):
    class Meta:
        model = OrderInformation


class UserRequestSchema(ModelSchema):
    class Meta:
        model = UserRequestEmbedded

