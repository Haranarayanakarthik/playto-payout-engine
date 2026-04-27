import random
from celery import shared_task
from django.db import transaction
from .models import *

def process_payout(id):
    payout = Payout.objects.get(id=payout_id)

    if payout.status != "pending":
        return

    payout.status = "processing"
    payout.save()

    outcome = random.random()

    with transaction.atomic():
        payout.refresh_from_db()

        if payout.status != "processing":
            return

        if outcome < 0.7:
            payout.status = "completed"
        else:
            payout.status = "failed"

            LedgerEntry.objects.create(
                merchant=payout.merchant,
                amount_paise=payout.amount_paise,
                entry_type="credit"
            )

        payout.save()
