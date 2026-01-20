import pytest
from unittest.mock import patch

@pytest.mark.django_db
def test_create_payout(api_client, payout_data):
    """Тест успешного создания заявки через POST"""
    response = api_client.post("/api/payouts/", data=payout_data, format="json")
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == "1000.00"
    assert data["currency"] == "USD"
    assert data["status"] == "pending"

@pytest.mark.django_db
def test_create_payout_triggers_celery_task(api_client, payout_data):
    """Тест, что при создании заявки запускается Celery-задача"""
    with patch("apps.payouts.tasks.process_payout.delay") as mock_task:
        response = api_client.post("/api/payouts/", data=payout_data, format="json")
        assert response.status_code == 201
        payout_id = response.json()["id"]
        mock_task.assert_called_once_with(payout_id)
