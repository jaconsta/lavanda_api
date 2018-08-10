from http import HTTPStatus

from flask import Blueprint, jsonify, request

from users.utils import user_from_authorization_headers
from .models import OrderInformation, UserAcceptedEmbedded
from .serializers import OrderInformationSchema
from utils.response import json_response

laundry_orders = Blueprint('laundry_orders', __name__)


@laundry_orders.route('/', methods=["POST"])
def new_laundry_order():
    """
    Request a laundry service.

    {
      "user_requesting": {"address": "asdf", "phone": "1234"},
      "laundry_details": [{"quantity": 2, "detail": "jean"}, {"quantity": 4, "detail": "camiseta"}]
    }
    ---
    tags:
      - Laundry_orders
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/OrderInformation'
    definitions:
      UserRequesting:
        type: object
        properties:
          address:
            type: string
          phone:
            type: string
      LaundryDetails:
        type: object
        properties:
          quantity:
            type: integer
          detail:
            type: string
      OrderInformation:
        type: object
        properties:
          id:
            type: string
            readOnly: true
          user_requesting:
            $ref: '#/definitions/UserRequesting'
          laundry_details:
            type: array
            items:
              $ref: '#/definitions/LaundryDetails'
          status:
            type: string
      OrderInformationResponse:
        type: object
        properties:
          message:
            type: string
          order:
            $ref: '#/definitions/OrderInformation'
      OrderInformationListResponse:
        type: object
        properties:
          message:
            type: string
          orders:
            type: array
            items:
              $ref: '#/definitions/OrderInformation'
    responses:
      201:
        description: Confirmation message the order was submitted.
        schema:
          $ref: '#/definitions/OrderInformation'

    """
    user = user_from_authorization_headers(request)
    laundry_order, errors = OrderInformationSchema(only=['user_requesting', 'laundry_details']).load(request.json)
    if errors:
        return json_response({'message': errors}, 500)
    print(laundry_order)
    laundry_order.user_requesting.user = user

    laundry_order.save()
    return json_response({'message': 'created', 'order': OrderInformationSchema().dump(laundry_order)[0]}, HTTPStatus.CREATED)


@laundry_orders.route('/', methods=["GET"])
def list_active():
    """
    Show all orders pending to accept from laundry people.

    ---
    tags:
      - Laundry_orders
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
    definitions:
      OrderInformationList:
        type: array
        items:
          $ref: '#/definitions/OrderInformation'
    responses:
      200:
        description: List of orders pending to accept.
        schema:
          $ref: '#/definitions/OrderInformationListResponse'
      401:
        description: Unauthorized.

    """
    user = user_from_authorization_headers(request)
    if not user.is_laundryman():
        return json_response({'message': 'Unauthorized'}, HTTPStatus.UNAUTHORIZED)

    order = OrderInformation(status=OrderInformation.ORDER_REQUESTED)
    return json_response({'message': 'created', 'order': OrderInformationSchema().dump(order, many=True)[0]})


@laundry_orders.route('/<order_id>', methods=["GET"])
def get(order_id):
    """
    Show a single laundry order.

    ---
    tags:
      - Laundry_orders
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
      - name: order_id
        in: path
        required: true
        type: string

    responses:
      200:
        description: Single order details.
        schema:
          $ref: '#/definitions/OrderInformationResponse'
      404:
        description: Not found.

    """

    order = OrderInformation(id=order_id)
    return json_response({'message': 'Order', 'order': OrderInformationSchema().dump(order)[0]})


@laundry_orders.route('/<order_id>/accept', methods=["POST"])
def accept(order_id):
    """
    Update the status of an order to accepted.

    ---
    tags:
      - Laundry_orders
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
      - name: order_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Laundry order with the status updated.
        schema:
          $ref: '#/definitions/OrderInformationResponse'

    """

    user = user_from_authorization_headers(request)
    if not user.is_laundryman():
        return json_response({'message': 'Unauthorized'}, 400)

    order = OrderInformation.objects.get(id=order_id)
    if order.status != OrderInformation.ORDER_REQUESTED:
        return json_response({'message': 'Invalid operation'}, 400)
    order.user_accepted = UserAcceptedEmbedded(full_name=user.full_name(), user=user, address=user.laundryman.address)
    order.status = OrderInformation.WAITING_PICKUP
    order.save()
    return json_response({'message': 'Accepted', 'order': OrderInformationSchema().dump(order).data})


@laundry_orders.route('/<order_id>/pickup', methods=["POST"])
def pickup(order_id):
    """
    Update the status to reflect the laundryman picked the laundry from the request person.

    ---
    tags:
      - Laundry_orders
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
      - name: order_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Laundry order with the status updated.
        schema:
          $ref: '#/definitions/OrderInformationResponse'

    """
    user = user_from_authorization_headers(request)
    order = OrderInformation(id=order_id)
    if order.user_accepted.user != user.id:
        return json_response({'message': 'Unauthorized'}, 400)
    order.order_is_pickup()

    return json_response({'message': 'pickup', 'order': OrderInformationSchema().dump(order)[0]})

