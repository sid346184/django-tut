from django.urls import path
from .views import WalletActionView, TransactionListView

urlpatterns = [
    path('wallet/credit/', WalletActionView.as_view(), {'action_type': 'CREDIT'}, name='wallet-credit'),
    path('wallet/debit/', WalletActionView.as_view(), {'action_type': 'DEBIT'}, name='wallet-debit'),
    path('wallet/transactions/', TransactionListView.as_view(), name='wallet-transactions'),
]
