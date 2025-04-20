from rest_framework import serializers


class TransactionInputSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(
        choices=['count', 'amount'], 
        default='count', 
    )
    type = serializers.ChoiceField(
        choices=['daily', 'weekly', 'monthly'], 
        default='daily', 
    )
    merchantId = serializers.IntegerField(
        required=False, 
        allow_null=True, 
    )