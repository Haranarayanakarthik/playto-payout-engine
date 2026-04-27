from django.urls import path
from payouts.views import dashboard, create_payout

urlpatterns = [
    path("api/v1/dashboard", dashboard),
    path("api/v1/payouts", create_payout),
]