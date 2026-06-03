from mongoengine import Document, StringField

class Asset(Document):
    asset_tag = StringField(required=True, unique=True)
    asset_type = StringField()
    brand = StringField()
    model = StringField()
    serial_number = StringField()
    department = StringField()
    status = StringField(default="Available")
    notes = StringField()
    meta = {'collection': 'assets'}