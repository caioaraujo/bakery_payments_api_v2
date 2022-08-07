from rest_framework import serializers

from branch.serializers import BranchResponseSerializer
from .models import Payment


class PaymentInputSerializer(serializers.ModelSerializer):
    """Payment input data serializer"""

    value = serializers.DecimalField(help_text="Payment value (R$)", required=True, max_digits=15, decimal_places=2)
    expiration_date = serializers.DateField(help_text="Date when payment will expires", required=True)
    branch = serializers.IntegerField(help_text="Branch identifier", required=True)

    class Meta:
        model = Payment
        fields = ("value", "expiration_date", "branch")


class PaymentPatchSerializer(serializers.ModelSerializer):
    """Payment fetch data serializer"""

    value = serializers.DecimalField(
        help_text="Payment value (R$). If not specified, " "it will try to pay the payment full value",
        required=False,
        max_digits=15,
        decimal_places=2,
    )

    class Meta:
        model = Payment
        fields = ("value",)


class PaymentResponseSerializer(serializers.ModelSerializer):
    """Custom payment response serializer"""

    branch = BranchResponseSerializer()

    class Meta:
        model = Payment
        fields = ("id", "value", "expiration_date", "branch", "is_paid", "date_payment")
