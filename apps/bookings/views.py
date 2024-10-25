from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .serializers import (
    BookingSerializer,
    BookSessionSerializer,
    BookSessionWithInsightorSerializer
)
from apps.profiles.serializers import InsightorSerializer
from apps.common.mixins import BookingMixin
from apps.common.response import CustomResponses
from .utils import (
        get_available_insightors, 
        is_insightor_available,
        get_available_time_slots
        )


tags = ["Bookings"]

class BookSessionAPIView(APIView):
    serializer_class = BookSessionSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=tags,
            summary="Get available consultant",
            description="""
                This endpoint returns all available insightors for the chosen date and time
            """
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        date_time = serializer.validated_data["date_time"]
        session_length = serializer.validated_data["num_hours"]
        insightors = get_available_insightors(date_time, session_length, request.user)

        if not insightors:
            return CustomResponses.success(message="No available insightor for the date and time you chose")

        insightor_serializer = InsightorSerializer(insightors, many=True)
        return CustomResponses.success(message="successfully retreived available consultants", data=insightor_serializer.data)


class BookingsListCreateAPIView(APIView, BookingMixin):
    serializer_class = BookingSerializer
    post_serializer = BookSessionWithInsightorSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
            tags=tags,
            summary="Return sessions booked by user",
            description="""
                This endpoint returns all user's bookings
            """
    )
    def get(self, request):
        bookings = self.get_user_bookings(request.user)

        if not bookings:
            return CustomResponses.success(message="You have no booking")

        serializer = self.serializer_class(bookings, many=True)
        return CustomResponses.success(message="Booking retreived successfully", data=serializer.data)

    @extend_schema(
            summary = "Book with insightor",
            description="""
            This endpoint books a session with insightor
            Note: 
                - The created session has a pending status, until after payment is made, the slot is no taken
            """,
            tags=tags,
            request=BookSessionWithInsightorSerializer,
            responses={"200": BookSessionWithInsightorSerializer},
    )
    def post(self, request):
        context = {
            "user": request.user       
        }
        serializer = self.post_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        insightor = serializer.validated_data["insightor"]
        date_time = serializer.validated_data["date_time"]
        session_length = serializer.validated_data["num_hours"]

        is_available = is_insightor_available(date_time, insightor, session_length)

        if not is_available:
            available_times = get_available_time_slots(date_time, insightor, session_length)

            if not available_times:
                return CustomResponses.error(message="No available time slot found, please try another day")
            
            return CustomResponses.success(message="Insightor is not available for chosen date and time but here is a list of times they are available", data=available_times)

        serializer.save(scheduled_for=date_time, user=request.user)

        return CustomResponses.success(message="Successfully acquired a time slot!", 
                                       data=serializer.data, status_code=201)


