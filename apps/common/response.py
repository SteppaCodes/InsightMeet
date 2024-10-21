from rest_framework.response import Response 


class CustomResponses:
    """
     A class for generating custom success amd error responses
    """

    @staticmethod
    def success(message: str, data: dict = None, status_code: int = 200) -> Response:
        response = {
            "status": "success",
            "message": message,
            "data": data
        }

        if data is None:
            response.pop("data")

        return Response(data=response, status=status_code)


    @staticmethod
    def error(message: str, status_code: int = 400) -> Response:
        response = {
            "status": "error",
            "message": message
        }

        return Response(data=response, status=status_code)
