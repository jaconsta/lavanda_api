from flask import Blueprint, request

from utils.response import json_response
from ..models import User
from ..utils import user_from_authorization_headers
from ..serializers.Users import LaundrymanDataSchema


users = Blueprint('users', __name__)


@users.route('/lavander', methods=["POST"])
def subscribe_as_lavander():
    """
    The user registers as laundry service provider.
    ---
    tags:
      - Users
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/Lavander'
    definitions:
      Lavander:
        type: object
        properties:
          address:
            type: string
          contact_phone:
            type: string
          approved:
            type: boolean
            readOnly: True
      LavanderResponse:
        type: object
        properties:
          message:
            type: string
          lavander:
            $ref: '#/definitions/Lavander'
    responses:
      200:
        description: Status as the lavander user.
        schema:
          $ref: '#/definitions/LavanderResponse'
        example:
          {
            "message": "Pending validation",
            "lavander": {
                "address": "Lavander place",
                "contact_phone": "3128485789",
                "approved": false,
            }
          }
    """
    user = user_from_authorization_headers(request)
    if User.LAUNDRYMAN in user.roles:
        return json_response({'message': 'Already laundryman'}, 400)
    laundryman, errors = LaundrymanDataSchema().load(request.json)
    if errors:
        return json_response({'message': errors}, 400)
    user.laundryman = laundryman
    user.roles.append(User.LAUNDRYMAN)
    user.save()
    return json_response({'message': 'Pending validation', 'lavander': LaundrymanDataSchema().dump(laundryman)[0]})
