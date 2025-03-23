from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet
from .serializers import WalletSerializer, OperationSerializer


class WalletView(APIView):
    """
    Эндпоинт для получения баланса кошелька.
    """
    def get(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        return Response(WalletSerializer(wallet).data)


class DepositView(APIView):
    """
    Эндпоинт для пополнения баланса кошелька.
    """
    @transaction.atomic()
    def post(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            wallet.deposit(serializer.validated_data['amount'])
            return Response(WalletSerializer(wallet).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawView(APIView):
    """
    Эндпоинт для снятия средств с кошелька.
    """
    @transaction.atomic()
    def post(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                wallet.withdraw(serializer.validated_data['amount'])
                return Response(WalletSerializer(wallet).data)
            except ValidationError as e:
                return Response({"error": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
