from .models import User
from utils.auth_parser import decode_jwt


def user_from_jwt(jwt):
    token = decode_jwt(jwt)
    print(token['email'])
    return User.objects.get(email=token['email'])


def user_from_authorization_headers(request):
    print(request.headers.get('Authorization'))
    return user_from_jwt(request.headers.get('Authorization'))
