import jwt


JWT_SECRET = 'xjl490hmx09zdto9'


def decode_jwt(token):
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
