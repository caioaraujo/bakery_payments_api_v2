from rest_framework import serializers

from payment.models import Payment
from .models import Branch


class BranchInputSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="Branch name. Maximum 100 characters.", required=True)
    current_balance = serializers.DecimalField(
        help_text="Branch's current balance.", required=True, max_digits=15, decimal_places=2
    )


class BranchResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ("id", "name", "current_balance", "previous_balance")


class PaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "value", "expiration_date", "is_paid")
