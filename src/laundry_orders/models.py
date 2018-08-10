from datetime import datetime

import mongoengine as me

from users.models import User


class UserRequestEmbedded(me.EmbeddedDocument):
    user = me.ReferenceField(User)
    address = me.StringField()
    phone = me.StringField()


class UserAcceptedEmbedded(me.EmbeddedDocument):
    user = me.ReferenceField(User)
    full_name = me.StringField()
    address = me.StringField()


class LaundryDetailsEmbedded(me.EmbeddedDocument):
    quantity = me.IntField()
    detail = me.StringField()


class StatusUpdateEmbedded(me.EmbeddedDocument):
    status = me.StringField()
    updated_at = me.DateTimeField(default=datetime.utcnow)


class OrderInformation(me.Document):
    user_requesting = me.EmbeddedDocumentField(UserRequestEmbedded)
    user_accepted = me.EmbeddedDocumentField(UserAcceptedEmbedded)

    pickup_time = me.DateTimeField()
    
    laundry_details = me.EmbeddedDocumentListField(LaundryDetailsEmbedded)

    ORDER_REQUESTED = 'ORDER_REQUESTED'
    WAITING_PICKUP = 'WAITING_PICKUP'
    ON_LAUNDRY = 'ON_LAUNDRY'
    STATUS_CHOICES = (
        ORDER_REQUESTED,
        WAITING_PICKUP,
        ON_LAUNDRY,
        'READY_TO_RETURN',
        'FINISHED',
        'CANCELED'
    )
    status = me.StringField(choices=STATUS_CHOICES, default=ORDER_REQUESTED)
    status_update = me.EmbeddedDocumentListField(StatusUpdateEmbedded)

    def order_is_pickup(self):
        self.laundry_details = datetime.utcnow()
        self.status.append(self.ON_LAUNDRY)
        self.save()
