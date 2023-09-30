from typing import Self

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .decorators import (
    serialized_request,
    serialized_response,
)
from .serializers import (
    TestGetRequestSerializer,
    TestGetResponseSerializer,
    TestPostRequestSerializer,
    TestPostResponseSerializer,
)

class TestResource(APIView):
    @serialized_response(TestGetResponseSerializer)
    @serialized_request(TestGetRequestSerializer)
    def get(self: Self, request: Request) -> Response:
        response_data: dict = {
            'name': 'Koki',
            'age': 20,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    @serialized_response(TestPostResponseSerializer)
    @serialized_request(TestPostRequestSerializer)
    def post(self: Self, request: Request) -> Response:
        response_data: dict = {
            'id': 1,
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)
