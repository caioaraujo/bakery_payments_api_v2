from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import BranchInputSerializer, BranchResponseSerializer
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

        result = {'message': _('Branch recorded successfully!'), 'data': serialized.data}
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

    def get(self, request, branch_id):
        """
        Returns a single branch
        """
        data = self.service.find_by_id(branch_id)

        if not data:
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        serialized = BranchResponseSerializer(data)

        return Response(serialized.data)
