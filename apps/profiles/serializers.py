from rest_framework import serializers
from .models import Insightor


class CompleteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insightor
        fields = [
            "specialization",
            "bio",
            "country",
            "experience_years",
            "available",
            "hourly_rate",
            "linkedin_url",
            "facebook_url",
            "website_url"
        ]

    def validate(self, attrs):
        experience_years = attrs["experiance_years"]
        if experience_years < 0:
            raise serializers.ValidationError({"error":"You cannot pick a number below 0"})
        

