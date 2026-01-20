# src/apps/payouts/tasks.py
import time
from celery import shared_task
from .models import Payout

@shared_task
def process_payout(payout_id):
    """
    Имитирует обработку выплаты:
    - Пауза (имитация внешнего запроса)
    - Логирование
    - Обновление статуса
    """
    try:
        payout = Payout.objects.get(id=payout_id)
    except Payout.DoesNotExist:
        return f"Payout {payout_id} not found"

    # Имитация обработки
    time.sleep(5)  # задержка 5 секунд
    payout.status = "processed"
    payout.save()
    return f"Payout {payout_id} processed"

