from django.utils.translation import ugettext as _
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import PaymentInputSerializer, PaymentPatchSerializer, PaymentResponseSerializer
from .services import PaymentService


class PaymentView(GenericAPIView):

    serializer_class = PaymentInputSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = PaymentService()

    def post(self, request):
        """
        Record a new payment.
        """
        params = request.data.copy()
        data = self.service.insert(params)
        serializer = PaymentResponseSerializer(data)

        result = {'detail': _('Payment recorded successfully!'), 'data': serializer.data}
        return Response(result)


class PaymentViewId(GenericAPIView):

    serializer_class = PaymentPatchSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = PaymentService()

    def patch(self, request, payment_id):
        """
        Update payment value. If payment value reach zero, the flag is_paid will be set to true.
        It will raise an error if:

        - Payment is already paid;
        - Expiration date has already passed;
        - Value is higher than amount available for payment;
        - Branch has no balance.
        """
        params = dict(
            value=request.data.get('value'), id=payment_id
        )
        data = self.service.pay(params)
        serializer = PaymentResponseSerializer(data)

        result = {'detail': _('Payment changed successfully!'), 'data': serializer.data}
        return Response(result)
