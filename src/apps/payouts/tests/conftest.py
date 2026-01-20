import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Клиент для тестирования DRF API"""
    return APIClient()

@pytest.fixture
def payout_data():
    """Данные для создания новой заявки"""
    return {
        "amount": 1000,
        "currency": "USD",
        "recipient_details": "Account 123456",
        "comment": "Test payout",
    }
