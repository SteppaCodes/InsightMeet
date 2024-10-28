from apps.profiles.models import Insightor
from rest_framework.response import Response
from rest_framework import status
from apps.common.response import CustomResponses
from django.db.models import Q
from apps.bookings.models import Booking
from apps.accounts.models import User
import uuid

class InsightorMixin:
    def get_insightor(self, insightor_id: uuid) -> Insightor:
        try:
            return Insightor.objects.get(id=insightor_id)
        except Insightor.DoesNotExist:
            return CustomResponses.error(message="Insightor does not exist",
                                         status_code=404
                                         )

    def get_insightor_info(sekf, insightor_id):
        """
        Get all details of the insightor.. suitable for profile pages
        """
        try:
            return Insightor.objects.prefetch_related("educations","certifications").get(id=insightor_id)
        except Insightor.DoesNotExist:
            return CustomResponses.error(message="Insightor does not exist",
                                         status_code=404
                                         )
        
    def get_insightors_list(self, filters: dict=None) -> list[Insightor]:
        allowed_filters = ["country", "specialization", "experience_years", "hourly_rate"]

        if not filters:
            return Insightor.objects.all()
        
        # create a dictionary for query params in allowed_filters
        query_filters = {key: value for key, value in filters.items() if key in allowed_filters}
        return Insightor.objects.filter(**query_filters)
        
        
class BookingMixin:
    def get_user_bookings(self, user: User) -> list[Booking]:
        return Booking.objects.filter(Q(user=user) | Q(insightor__user=user))

    def get_done_bookings(self, user: User) -> list[Booking]:
        return self.get_user_bookings(user).filter(is_done=True)

    def get_pending_bookings(self, user: User) -> list[Booking]:
        return self.get_user_bookings(user).filter(status="pending")
    
    def get_pending_booking(self, booking_id: uuid) -> Booking:
        try:
            return Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return None