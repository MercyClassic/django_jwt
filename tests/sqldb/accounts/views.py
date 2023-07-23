from rest_framework import status
from tests.base.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TestAuthBackendAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
