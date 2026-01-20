import pytest
from apps.payouts.models import Payout

@pytest.mark.django_db
def test_patch_status_pending(api_client):
    """
    Успешное изменение статуса заявки, если текущий статус pending.
    """
    payout = Payout.objects.create(
        amount=100,
        currency="USD",
        recipient_details="test recipient"
    )

    response = api_client.patch(
        f"/api/payouts/{payout.id}/",
        {"status": "processed"},
        format="json"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processed"
    # Другие поля остались без изменений
    assert float(data["amount"]) == 100
    assert data["currency"] == "USD"
    assert data["recipient_details"] == "test recipient"


@pytest.mark.django_db
def test_patch_forbidden_fields_on_processed(api_client):
    """
    Попытка изменить amount/currency/recipient_details после обработки
    должна вернуть ошибки для всех запрещённых полей.
    """
    payout = Payout.objects.create(
        amount=100,
        currency="USD",
        recipient_details="recipient",
        status="processed"
    )

    response = api_client.patch(
        f"/api/payouts/{payout.id}/",
        {
            "amount": 200,
            "currency": "RUB",
            "recipient_details": "new recipient",
        },
        format="json"
    )

    assert response.status_code == 400
    data = response.json()

    # Проверяем, что все запрещённые поля вернули ошибки
    for field in ["amount", "currency", "recipient_details"]:
        assert field in data
        assert data[field] == [f"Поле '{field}' нельзя менять для заявки со статусом 'processed'"]

    # Поля в базе остались без изменений
    payout.refresh_from_db()
    assert payout.amount == 100
    assert payout.currency == "USD"
    assert payout.recipient_details == "recipient"
    assert payout.status == "processed"


@pytest.mark.django_db
def test_patch_comment_on_processed(api_client):
    """
    Для уже обработанных заявок разрешено менять только comment.
    """
    payout = Payout.objects.create(
        amount=100,
        currency="USD",
        recipient_details="recipient",
        status="processed",
        comment="initial comment"
    )

    response = api_client.patch(
        f"/api/payouts/{payout.id}/",
        {"comment": "updated comment"},
        format="json"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["comment"] == "updated comment"

    payout.refresh_from_db()
    assert payout.comment == "updated comment"
    # Другие поля остались без изменений
    assert payout.amount == 100
    assert payout.currency == "USD"
    assert payout.recipient_details == "recipient"
    assert payout.status == "processed"


@pytest.mark.django_db
def test_patch_invalid_status_transition(api_client):
    """
    Проверка запрета на невозможные переходы статуса
    """
    payout = Payout.objects.create(
        amount=100,
        currency="USD",
        recipient_details="recipient",
        status="processed"
    )

    response = api_client.patch(
        f"/api/payouts/{payout.id}/",
        {"status": "pending"},  # недопустимый переход
        format="json"
    )

    assert response.status_code == 400
    data = response.json()
    print(data)
    assert "status" in data
    assert data["status"] == ["Невозможное изменение статуса: processed -> pending"]


    # Статус в базе остался без изменений
    payout.refresh_from_db()
    assert payout.status == "processed"
