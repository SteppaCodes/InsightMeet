from rest_framework import serializers
from .models import Insightor, Education, Certification


class InsightorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insightor
        exclude = ["created_at", "updated_at"]


class CreateUpdateInsightorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insightor
        fields = [
            "id",
            "specialization",
            "bio",
            "country",
            "experience_years",
            "available",
            "available_days",
            "work_start",
            "work_end",
            "hourly_rate",
            "resume",
            "linkedin_url",
            "facebook_url",
            "website_url"
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        experience_years = attrs["experience_years"]
        if experience_years < 0:
            raise serializers.ValidationError({"error":"You cannot pick a number below 0"})

        return attrs

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "institution",
            "degree",
            "field_of_study",
            "start_date",
            "end_date"
        ]

        read_only_fields = ["id"]

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = [
            "id",
            "name",
            "issuing_organization",
            "issue_date"
        ]

        read_only_fields = ["id"]