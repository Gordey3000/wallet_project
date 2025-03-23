from django.test import TransactionTestCase
from django.core.exceptions import ValidationError
from django.db import connection
from .models import Wallet
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor


class WalletTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        """Создаем тестовый кошелек перед каждым тестом"""
        self.wallet = Wallet.objects.create()

    def tearDown(self):
        """Принудительное завершение соединений после каждого теста"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_terminate_backend(pid) FROM "
                           "pg_stat_activity WHERE datname = "
                           "current_database() AND pid <> pg_backend_pid();")

    def test_deposit_success(self):
        """Тест успешного пополнения кошелька"""
        self.wallet.deposit(Decimal("100.00"))
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("100.00"))

    def test_withdraw_success(self):
        """Тест успешного снятия средств"""
        self.wallet.deposit(Decimal("100.00"))
        self.wallet.withdraw(Decimal("50.00"))
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("50.00"))

    def test_withdraw_insufficient_funds(self):
        """Тест снятия средств при недостаточном балансе"""
        with self.assertRaises(ValidationError):
            self.wallet.withdraw(Decimal("50.00"))

    def test_concurrent_deposit(self):
        """Тест конкурентного пополнения (многопоточное пополнение)"""
        def deposit():
            self.wallet.refresh_from_db()
            self.wallet.deposit(Decimal("50.00"))

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(deposit) for _ in range(5)]
            for future in futures:
                future.result()

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("250.00"))

    def test_concurrent_withdraw(self):
        """Тест конкурентного снятия средств (многопоточное списание)"""
        self.wallet.deposit(Decimal("200.00"))

        def withdraw():
            self.wallet.refresh_from_db()
            try:
                self.wallet.withdraw(Decimal("50.00"))
            except ValidationError:
                pass

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(withdraw) for _ in range(5)]
            for future in futures:
                future.result()

        self.wallet.refresh_from_db()
        self.assertIn(self.wallet.balance, [Decimal("0.00"), Decimal("50.00")])
