from django.db import transaction
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Wallet, Transaction
from customers.models import Customer
from .serializers import TransactionSerializer, CreditDebitSerializer

class WalletActionView(APIView):
    def post(self, request, action_type):
        serializer = CreditDebitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        customer_id = serializer.validated_data['customer_id']
        points = serializer.validated_data['points']
        idempotency_key = serializer.validated_data['idempotency_key']
        meta = serializer.validated_data.get('meta', {})

        customer = get_object_or_404(Customer, id=customer_id, is_active=True)
        
        # Ensure wallet exists
        wallet, created = Wallet.objects.get_or_create(customer=customer)

        # Idempotency check
        if Transaction.objects.filter(idempotency_key=idempotency_key).exists():
            existing_txn = Transaction.objects.get(idempotency_key=idempotency_key)
            return Response(TransactionSerializer(existing_txn).data, status=status.HTTP_200_OK)

        try:
            with transaction.atomic():
                # Lock the wallet row
                wallet = Wallet.objects.select_for_update().get(id=wallet.id)

                if action_type == 'DEBIT':
                    if wallet.balance < points:
                        return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
                    wallet.balance -= points
                elif action_type == 'CREDIT':
                    wallet.balance += points
                
                wallet.save()

                txn = Transaction.objects.create(
                    wallet=wallet,
                    type=action_type,
                    points=points,
                    idempotency_key=idempotency_key,
                    meta=meta
                )
                
                return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        queryset = Transaction.objects.all().order_by('-created_at')
        customer_id = self.request.query_params.get('customer_id')
        txn_type = self.request.query_params.get('type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if customer_id:
            queryset = queryset.filter(wallet__customer_id=customer_id)
        if txn_type:
            queryset = queryset.filter(type=txn_type)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
            
        return queryset
