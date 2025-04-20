from mongoengine import Document, ObjectIdField, IntField, FloatField, DateTimeField
from django.utils import timezone

class Transaction(Document):
    _id = ObjectIdField(required=True, primary_key=True)  
    merchantId = IntField(required=True)  
    amount = FloatField(required=True, min_value=0) 
    createdAt = DateTimeField(default=timezone.now())

