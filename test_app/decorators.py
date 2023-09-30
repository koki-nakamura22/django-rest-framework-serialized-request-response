import inspect
from pprint import pprint
from types import FrameType
from typing import Callable, Tuple, List

from django.forms import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer


class RequestError(Exception):
    pass


def _get_calling_class_and_function_name() -> Tuple[str | None, str]:
    frames: List[inspect.FrameInfo] = inspect.stack()

    for frame_info in frames:
        function: str = frame_info.function
        if function in ["get", "post", "put", "delete", "patch", "head", "options"]:
            class_name: str | None = None
            try:
                currentframe: FrameType | None = inspect.currentframe()
                if currentframe and currentframe.f_back and currentframe.f_back.f_back:
                    class_name = currentframe.f_back.f_back.f_locals['self'].__class__.__name__
            except (KeyError, AttributeError):
                class_name = None
            return class_name, function

    return None, "Unknown"


def serialized_request(serializer_class: Serializer) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(view, request: Request, *args, **kwargs) -> None:
            serializer: Serializer | None = None
            if func.__name__ == 'get':
                serializer = serializer_class(
                    data=request.query_params)
            else:
                serializer = serializer_class(data=request.data)
            if not serializer.is_valid():
                raise RequestError(serializer.errors)
            return func(view, request, *args, **kwargs)
        return wrapper
    return decorator


def serialized_response(serializer_class: Serializer) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(view, request: Request, *args, **kwargs) -> Response:
            try:
                # This variable type is not attached response type hinting because it can be HttpResponse or StreamingHttpResponse.
                response = func(view, request, *args, **kwargs)
                serializer: Serializer = serializer_class(data=response.data)
                if not serializer.is_valid():
                    raise ValidationError(serializer.errors)
                if 100 <= response.status_code and response.status_code <= 299:
                    return Response(data=serializer.data, status=response.status_code)
                else:
                    pprint(serializer_class(response.data).data)
                    return Response(status=response.status_code)
            except Exception as e:
                class_name, function_name = _get_calling_class_and_function_name()
                class_type: str = 'RequestClass' if isinstance(e, RequestError) else 'ResponseClass'
                print(
                    f"Error in {class_type}: {class_name}, Function: {function_name}, error details: {e}")
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return wrapper
    return decorator
