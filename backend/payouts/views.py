from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Sum, Case, When, F, BigIntegerField
from .models import Merchant, LedgerEntry, Payout
from .tasks import process_payout


# ✅ Ledger-based balance (DB-level, no Python math)
def get_balance(merchant):
    result = LedgerEntry.objects.filter(merchant=merchant).aggregate(
        balance=Sum(
            Case(
                When(entry_type="credit", then=F("amount_paise")),
                When(entry_type="debit", then=-F("amount_paise")),
                output_field=BigIntegerField()
            )
        )
    )
    return result["balance"] or 0


# ✅ Dashboard API
@api_view(["GET"])
def dashboard(request):
    m, _ = Merchant.objects.get_or_create(name="Default Merchant")

    return Response({
        "balance": get_balance(m),
        "payouts": list(Payout.objects.values())
    })

# ✅ Create payout (core logic)
@api_view(["POST"])
def create_payout(request):
    merchant = Merchant.objects.first()

    if not merchant:
        return Response({"error": "No merchant found"}, status=400)

    # 🔴 Idempotency key
    key = request.headers.get("Idempotency-Key")
    if not key:
        return Response({"error": "Missing Idempotency-Key"}, status=400)

    # 🔴 Validate amount
    try:
        amount = int(request.data.get("amount_paise", 0))
    except:
        return Response({"error": "Invalid amount format"}, status=400)

    if amount <= 0:
        return Response({"error": "Amount must be > 0"}, status=400)

    # 🔁 Idempotency check
    existing = Payout.objects.filter(
        merchant=merchant,
        idempotency_key=key
    ).first()

    if existing:
        return Response({
            "id": existing.id,
            "status": existing.status
        })

    # 🔐 Concurrency-safe transaction
    with transaction.atomic():
        # Lock merchant ledger rows
        LedgerEntry.objects.select_for_update().filter(merchant=merchant)

        # Recompute balance inside lock
        balance = get_balance(merchant)

        if balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        # Create payout
        payout = Payout.objects.create(
            merchant=merchant,
            amount_paise=amount,
            idempotency_key=key,
            status="pending"
        )

        # Hold funds (debit entry)
        LedgerEntry.objects.create(
            merchant=merchant,
            amount_paise=amount,
            entry_type="debit"
        )

    # 🚀 Async processing
    process_payout.delay(payout.id)

    return Response({
        "id": payout.id,
        "status": "pending"
    })
