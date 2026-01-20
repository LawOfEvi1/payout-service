# apps/payouts/views.py
from rest_framework import generics
from .models import Payout
from .serializers import PayoutSerializer

class PayoutListCreateView(generics.ListCreateAPIView):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer

class PayoutDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
