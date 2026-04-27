from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Sum, Case, When, F, BigIntegerField
from .models import Merchant, LedgerEntry, Payout
from .tasks import process_payout


# ✅ Ensure merchant always exists
def get_merchant():
    merchant, _ = Merchant.objects.get_or_create(name="Default Merchant")

    # FORCE add balance (temporary fix)
    if get_balance(merchant) == 0:
        LedgerEntry.objects.create(
            merchant=merchant,
            amount_paise=100000,
            entry_type="credit"
        )

    return merchant


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
    merchant = get_merchant()

    return Response({
        "balance": get_balance(merchant),
        "payouts": list(Payout.objects.values())
    })


# ✅ Create payout
@api_view(["POST"])
def create_payout(request):
    merchant = get_merchant()   # 🔥 FIXED HERE

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
        LedgerEntry.objects.select_for_update().filter(merchant=merchant)

        balance = get_balance(merchant)

        if balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        payout = Payout.objects.create(
            merchant=merchant,
            amount_paise=amount,
            idempotency_key=key,
            status="pending"
        )

        # Hold funds
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
