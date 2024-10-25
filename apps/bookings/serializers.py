from rest_framework import serializers
from .models import Booking
from django.utils import timezone
from datetime import datetime


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class BookSessionSerializer(serializers.ModelSerializer):
    day = serializers.IntegerField(write_only=True)
    month = serializers.IntegerField(write_only=True)
    year = serializers.IntegerField(write_only=True)
    hour = serializers.IntegerField(write_only=True)
    minute = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields=  [
            "subject",
            "user_needs",
            "num_hours",
            "year",
            "month",
            "day",
            "hour",
            "minute"
        ]

    def validate(self, attrs: dict) -> dict:
        year = attrs.get("year")
        month = attrs.get("month")
        day = attrs.get("day")
        hour = attrs.get("hour")
        minute = attrs.get("minute")
        session_length = attrs.get("num_hours")

        #create datetime object
        date_time = timezone.make_aware(datetime(year, month, day, hour, minute))

        if session_length < 1:
            raise serializers.ValidationError({"error": "The number of hours cannot be less tham 1"})

        #ensure that the chosen date is not in the past
        if date_time.date() < timezone.now().date():
            raise serializers.ValidationError({"error": "Sorry, you cannot pick a date in the past"})

        #if date is valid, add datetime to the validated data dictionary
        attrs["date_time"] = date_time
        return attrs

    def create(self, validated_data: dict) -> Booking:

        day = validated_data.pop('day')
        month = validated_data.pop('month')
        year = validated_data.pop('year')
        hour = validated_data.pop('hour')
        minute = validated_data.pop('minute')
        date_time = validated_data.pop("date_time")

        booking = Booking.objects.create(
            **validated_data
        )
        return booking


class BookSessionWithInsightorSerializer(BookSessionSerializer):
    class Meta(BookSessionSerializer.Meta):
        fields = BookSessionSerializer.Meta.fields + ["insightor"]

    def validate(self, attrs:dict):
        attrs = super().validate(attrs)

        insightor = attrs["insightor"]
        user = self.context["user"]
        if insightor.user.id == user.id:
            raise serializers.ValidationError({"error": "You cannot book a session with yourself"})

    
