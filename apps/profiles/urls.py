from django.urls import path
from .views import (
    InsightorsListCreateAPIView,
    EducationListCreateAPIView,
    CertificationsListCreateAPIView
)

urlpatterns = [
    path("insightors/", InsightorsListCreateAPIView.as_view()),
    path("education/<uuid:insightor_id>/", EducationListCreateAPIView.as_view()),
    path("certifications/<uuid:insightor_id>/", CertificationsListCreateAPIView.as_view()),
]