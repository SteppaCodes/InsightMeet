from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Insightor
from .serializers import CompleteProfileSerializer


class CompleteInsightorProfileView(APIView):
    serializer_class = CompleteProfileSerializer

    def patch(self, request, id):
        insightor = Insightor.objects.get(id=id)
        serializer = self.serializer_class(insightor, data=request.data)
        serializer.is_valid(raise_exceptions=True)
        serializer.save()

        return Response({"data":serializer.data, "success":"profile updated successfully"}, status=status.HTTP_200_OK)



