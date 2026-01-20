# serializers.py
from rest_framework import serializers
from .models import Payout

class PayoutSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Payout
        fields = [
            'id',
            'amount',
            'currency',
            'recipient_details',
            'status',
            'comment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']



    # ---------- Валидация отдельных полей ----------
    def validate_status(self, value):
        instance = getattr(self, 'instance', None)
        if instance:
            current_status = instance.status
            allowed_transitions = {
                'pending': ['processed', 'failed'],
                'processed': [],
                'failed': [],
            }

            if value != current_status and value not in allowed_transitions[current_status]:
                raise serializers.ValidationError(
                    f"Невозможное изменение статуса: {current_status} -> {value}"
                )
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть положительным числом")
        return value

    def validate_currency(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Валюта должна быть в формате ISO 4217 (например: RUB, USD)")
        return value.upper()

    def validate_recipient_details(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Реквизиты получателя слишком короткие")
        return value

    # ---------- Общая валидация ----------

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        if instance and instance.status != 'pending':
            forbidden_fields = ['amount', 'currency', 'recipient_details']
            errors = {}
            for field in forbidden_fields:
                if field in attrs:
                    errors[field] = [f"Поле '{field}' нельзя менять для заявки со статусом '{instance.status}'"]
            if errors:
                raise serializers.ValidationError(errors)
        return attrs

    def update(self, instance, validated_data):
        """
        Применяем изменения после валидации
        """
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
    def create(self, validated_data):
        # Вынесем статус явно, чтобы DRF точно не перезаписывал поля
        return Payout.objects.create(**validated_data)
