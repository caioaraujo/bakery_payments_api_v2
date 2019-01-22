from django.utils.translation import ugettext as _
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .filters import PaymentFilterBackend
from .serializers import BranchInputSerializer, BranchResponseSerializer, PaymentResponseSerializer
from .services import BranchService


class BranchView(GenericAPIView):

    serializer_class = BranchInputSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BranchService()

    def post(self, request):
        """
        Records a new branch
        """
        params = request.data.copy()
        data = self.service.insert(params)
        serialized = BranchResponseSerializer(data)

        result = {'detail': _('Branch recorded successfully!'), 'data': serialized.data}
        return Response(result)

    def get(self, request):
        """
        Returns a list of branches
        """
        data = self.service.find()
        serialized = BranchResponseSerializer(data, many=True)

        return Response(serialized.data)


class BranchViewId(GenericAPIView):

    serializer_class = BranchInputSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BranchService()

    def put(self, request, branch_id):
        """
        Update branch data
        """
        params = request.data.copy()
        params['id'] = branch_id
        data = self.service.update(params)
        serialized = BranchResponseSerializer(data)

        result = {'detail': _('Branch updated successfully!'), 'data': serialized.data}
        return Response(result)

    def get(self, request, branch_id):
        """
        Returns a single branch
        """
        data = self.service.find_by_id(branch_id)

        serialized = BranchResponseSerializer(data)

        return Response(serialized.data)

    def delete(self, request, branch_id):
        """
        Removes a single branch
        """
        self.service.delete(branch_id)

        result = {'detail': _('Branch deleted successfully!')}
        return Response(result)


class BranchPaymentsView(GenericAPIView):

    filter_backends = [PaymentFilterBackend]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BranchService()

    def get(self, request, branch_id):
        """
        Returns all branch payments
        """
        params = request.GET.dict()
        params['branch'] = branch_id
        data = self.service.find_payments(params)
        serialized = PaymentResponseSerializer(data, many=True)

        return Response(serialized.data)
