from django.db import models

class Merchant(models.Model):
    name = models.CharField(max_length=100)

class LedgerEntry(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount_paise = models.BigIntegerField()
    entry_type = models.CharField(max_length=10)  # credit/debit

class Payout(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount_paise = models.BigIntegerField()
    status = models.CharField(max_length=20, default="pending")
    idempotency_key = models.CharField(max_length=255)
    attempts = models.IntegerField(default=0)

    class Meta:
        unique_together = ("merchant", "idempotency_key")