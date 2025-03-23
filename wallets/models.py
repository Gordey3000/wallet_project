import uuid
from django.db import models, transaction
from django.core.exceptions import ValidationError


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def deposit(self, amount):
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(uuid=self.uuid)
            wallet.balance += amount
            wallet.save()

    def withdraw(self, amount):
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(uuid=self.uuid)
            if wallet.balance < amount:
                raise ValidationError("Insufficient balance")
            wallet.balance -= amount
            wallet.save()
