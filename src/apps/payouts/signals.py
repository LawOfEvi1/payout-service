# src/apps/payouts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payout
from .tasks import process_payout

@receiver(post_save, sender=Payout)
def payout_created(sender, instance, created, **kwargs):
    if created:
        process_payout.delay(instance.id)
