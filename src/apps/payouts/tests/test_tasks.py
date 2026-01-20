import pytest
from apps.payouts.models import Payout
from apps.payouts.tasks import process_payout

@pytest.mark.django_db
def test_process_payout_task(payout_data):
    """Тест самой Celery-задачи"""
    payout = Payout.objects.create(**payout_data)

    # Запускаем задачу синхронно
    result = process_payout(payout.id)

    payout.refresh_from_db()
    assert payout.status == "processed"
    assert result == f"Payout {payout.id} processed"
