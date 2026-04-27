import random
from django.db import transaction
from .models import Payout, LedgerEntry


def process_payout(payout_id):
    payout = Payout.objects.get(id=payout_id)

    # Ignore if already processed
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

            # Refund money
            LedgerEntry.objects.create(
                merchant=payout.merchant,
                amount_paise=payout.amount_paise,
                entry_type="credit"
            )

        payout.save()
