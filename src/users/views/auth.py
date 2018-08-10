from flask import Blueprint, jsonify, request
import jwt

from utils.auth_parser import JWT_SECRET
from utils.response import json_response
from ..serializers.Users import RegisterSchema
from ..models import User


HASH_NAME = 'sha256'
# TODO: For salt, should use python3.7 scrypt. Should generate new salt per password os.urandom().
SALT = 'xjl490hmx09zdto9'
ITERATIONS = 1000
users_register = Blueprint('users_register', __name__)


@users_register.route('/register', methods=["POST"])
def register():
    """
    Register a new user into the platform.
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/User'
    definitions:
      User:
        type: object
        properties:
          id:
            type: string
            readOnly: true
          first_name:
            type: string
          last_name:
            type: string
          email:
            type: string
            format: email
          password:
            type: string
            format: password
      UserResponse:
        type: object
        properties:
          message:
            type: string
          user:
            $ref: '#/definitions/User'

    responses:
      200:
        description: Information of the user created
        schema:
          $ref: '#/definitions/UserResponse'
        example:
          {
              "message": "created",
              "user": {
                "email": "a@mail.com",
                "first_name": "J",
                "id": "5b6861188959d33e744515e5",
                "last_name": "Consta",
                "password": "123456"
              }
          }
      500:
        description: Invalid form.
    """
    user, errors = RegisterSchema(only=['first_name', 'last_name', 'email', 'password']).load(request.json)
    if errors:
        return json_response({'message': errors}, 500)
    try:
        user.save()
    except:
        return json_response({'error': 'Could not save user.'})
    return json_response({'message': 'created', 'user': RegisterSchema().dump(user)[0]})


@users_register.route('/login', methods=["POST"])
def login():
    """
    Login the user to get session key.
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/UserCredentials'
    definitions:
      UserCredentials:
        type: object
        properties:
          email:
            type: string
            format: email
          password:
            type: string
            format: password
      JwtToken:
        type: object
        properties:
          token:
            type: string

    responses:
      200:
        description: JWT session key.
        schema:
          $ref: '#/definitions/JwtToken'
      500:
        description: Invalid form.
      400:
        description: Wrong user.
    """
    user_form, errors = RegisterSchema(only=['email', 'password']).load(request.json)
    if errors:
        return json_response({'error': errors}, 500)
    try:
        user = User.objects.get(email=user_form.email)
    except:
        return json_response({'error': 'Wrong User'}, 400)

    if user.password != user_form.password:
        return json_response({'error': 'Wrong User'}, 400)

    encoded = jwt.encode({'some': 'payload', 'email': user.email}, JWT_SECRET, algorithm='HS256').decode('utf-8')
    return jsonify({'token': encoded})
