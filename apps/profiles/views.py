from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema

from .models import Insightor, Education, Certification
from .serializers import (
    CreateInsightorProfileSerializer,
    EducationSerializer,
    CertificationSerializer,
    InsightorSerializer
)
from apps.common.mixins import InsightorMixin
from apps.common.response import CustomResponses

class InsightorsListCreateAPIView(APIView, InsightorMixin):
    serializer_class = InsightorSerializer
    post_serializer = CreateInsightorProfileSerializer

    def get(self, request):
        filters = request.query_params    
        insightors = self.get_insightors_list(filters)

        if not insightors.exists():
           return CustomResponses.success(
               message="No consultants found for the given filters"
           )

        serializer = self.serializer_class(insightors, many=True)
        return CustomResponses.success(
            message="Insightors retreived successfully",
            data=serializer.data
        )

    def post(self, request):
        serializer = self.post_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.is_insightor = True
        user.save()

        serializer.save(
            user=user
        )

        return CustomResponses.success(
            message="Insightor created successfully",
            data=serializer.data,
            status_code=201
        )
        
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == "GET":
            return [AllowAny()]


class EducationListCreateAPIView(APIView, InsightorMixin):
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, insightor_id):

        insightor = self.get_insightor(insightor_id)
        
        educations = Education.objects.select_related('insightor').filter(insightor=insightor)
        if not educations.exists():
            return CustomResponses.success(
                message=f"{insightor.user.full_name} has not added any information concerning their education"
                )

        serializer = self.serializer_class(educations, many=True)
        return CustomResponses.success(
            message=f"education info for {insightor.user.full_name} retreived successfully",
            data=serializer.data
            )

    def post(self, request, insightor_id):
        insightor = self.get_insightor(insightor_id)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            insightor=insightor
        )

        return CustomResponses.succes(
            message="Education information added successfully",
            data = serializer.data,
            status_code=201
        )
        

class CertificationsListCreateAPIView(APIView, InsightorMixin):
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, insightor_id):
        insightor = self.get_insightor(insightor_id)
        
        certifications = Certification.objects.select_related('insightor').filter(insightor=insightor)
        if not certifications.exists():
            return CustomResponses.error(
                message= f"{insightor.user.full_name} has not added any certifications"
            )

        serializer = self.serializer_class(certifications, many=True)
        return CustomResponses.success(
            message=f"certifications for {insightor.user.full_name} retreived successfully",
            data=serializer.data
        )

    def post(self, request, insightor_id):
        insightor = self.get_insightor(insightor_id)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            insightor=insightor
        )
        return CustomResponses.success(
            message="Education information added successfully",
            data = serializer.data,
            status_code=201
        )
