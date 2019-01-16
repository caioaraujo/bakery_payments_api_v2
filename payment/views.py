from django.utils.translation import ugettext as _
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import PaymentInputSerializer, PaymentResponseSerializer
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
        serialized = PaymentResponseSerializer(data)

        result = {'detail': _('Payment recorded successfully!'), 'data': serialized.data}
        return Response(result)
