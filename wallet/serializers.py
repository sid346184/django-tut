from rest_framework import serializers
from .models import Wallet, Transaction

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'customer', 'balance']
        read_only_fields = ['balance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'type', 'points', 'idempotency_key', 'created_at', 'meta']
        read_only_fields = ['created_at']

class CreditDebitSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    points = serializers.IntegerField(min_value=1)
    idempotency_key = serializers.CharField(max_length=255)
    meta = serializers.JSONField(required=False, default=dict)
