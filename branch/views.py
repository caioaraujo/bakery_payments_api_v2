from django.utils.translation import ugettext as _
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
