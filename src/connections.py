from mongoengine import connect


def mongo_connect(url=None):
    connect(host='mongodb://localhost:32768/lavanda_api')
    print('Connected to Database')
