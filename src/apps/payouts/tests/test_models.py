import pytest
from apps.payouts.models import Payout

@pytest.mark.django_db
def test_create_payout(payout_data):
    # Используем данные из фикстуры
    payout = Payout.objects.create(**payout_data)
    assert payout.id is not None
    assert payout.status == "pending"
    assert str(payout) == f"{payout.id} - {payout.amount} {payout.currency}"

