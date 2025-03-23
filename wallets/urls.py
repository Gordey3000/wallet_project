from django.urls import path
from .views import WalletView, DepositView, WithdrawView

urlpatterns = [
    path('<uuid:wallet_uuid>/', WalletView.as_view(),
         name='wallet_detail'),
    path('<uuid:wallet_uuid>/deposit/', DepositView.as_view(),
         name='deposit'),
    path('<uuid:wallet_uuid>/withdraw/', WithdrawView.as_view(),
         name='withdraw'),
]
