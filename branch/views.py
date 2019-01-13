from django.utils.translation import ugettext as _
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import BranchInputSerializer
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

        result = {'message': _('Branch recorded successfully!'), 'data': data}
        return Response(result)
