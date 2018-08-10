from datetime import datetime

import mongoengine as me


class Address(me.EmbeddedDocument):
    address = me.StringField(required=True)
    default = me.BooleanField(default=False)
    phone = me.IntField()


class LaundrymanDataEmbedded(me.EmbeddedDocument):
    address = me.StringField(required=True)
    contact_phone = me.StringField(required=True)
    approved = me.BooleanField(default=False)


class User(me.Document):
    # Basic information
    first_name = me.StringField(required=True, max_length=100)
    last_name = me.StringField(required=True, max_length=100)
    phone = me.IntField()

    # Default Login info
    email = me.EmailField(unique=True)
    password = me.StringField()

    # Authorization
    CLIENT = 'CLIENT'
    LAUNDRYMAN = 'LAUNDRYMAN'
    ADMIN = 'ADMIN'
    SUSPENDED = 'SUSPENDED'
    ROLE_CHOICES = (
        CLIENT,
        LAUNDRYMAN,
        ADMIN,
        SUSPENDED
    )
    roles = me.ListField(me.StringField(choices=ROLE_CHOICES), default=lambda: ['CLIENT'])

    # Pickup information
    addresses = me.EmbeddedDocumentListField(Address)

    # Specific role information
    laundryman = me.EmbeddedDocumentField(LaundrymanDataEmbedded)

    # Meta
    updated_at = me.DateTimeField(default=datetime.utcnow)

    def is_laundryman(self):
        return self.LAUNDRYMAN in self.roles

    def full_name(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)

