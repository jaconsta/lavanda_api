from flask import Flask
from flasgger import Swagger

from connections import mongo_connect

from users.views.auth import users_register
from users.views.users import users
from laundry_orders.views import laundry_orders


def app_factory(debug=False):
    app = Flask(__name__)
    app.debug = debug

    # set up your database
    mongo_connect()

    # set up third-party libraries
    Swagger(app)

    # add your modules
    app.register_blueprint(users_register, url_prefix='/api/auth')
    app.register_blueprint(users, url_prefix='/api/users')
    app.register_blueprint(laundry_orders, url_prefix='/api/laundry_orders')


    return app


if __name__ == "__main__":
    app = app_factory(debug=True)
    app.run()
