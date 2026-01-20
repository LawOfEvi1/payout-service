# apps/payouts/urls.py
from django.urls import path
from .views import PayoutListCreateView, PayoutDetailView

urlpatterns = [
    path("", PayoutListCreateView.as_view(), name="payout-list-create"),
    path("<int:pk>/", PayoutDetailView.as_view(), name="payout-detail"),
]
