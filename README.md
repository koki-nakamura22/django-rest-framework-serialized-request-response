# django-rest-framework-serialized-request-response

This is an example project that hides serializer request parameters and response data checks processing.

## Motivation

I did not want to write check parameters by serializer code repeatedly because iterative operations will make a lot of mistakes.  
Also, it is not good for our mental health. Simple iterative operations must be avoided always. This is a truth of the world.

## Usage

Copy the decorators.py in this project to your project, import it, and then attach it to API methods.  
When attaching decorators, serialized_request must always be executed first.  
It means serialized_request decorator is always needed to be here just above methods.

Example.
```python
from .decorators import (
    serialized_request,
    serialized_response,
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
```


## Processing Sequence Overview

1. serialized_request decorator checks request parameters and query parameters. When the parameters and serializer definition do not match, output an error message to the console only on the server side then return a 500 response.
2. Runs the code of the function to which the decorator is attached.
3. serialized_response decorator checks the method result. When the result and serializer definition do not match, output an error message to the console only on the server side then return a 500 response.

