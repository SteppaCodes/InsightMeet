from apps.profiles.models import Insightor
from rest_framework.response import Response
from rest_framework import status
from apps.common.response import CustomResponses


class InsightorMixin:
    def get_insightor(self, insightor_id):
        try:
            return Insightor.objects.get(id=insightor_id)
        except Insightor.DoesNotExist:
            return CustomResponses.error(message="Insightor does not exist",
                                         status_code=404
                                         )
        
    def get_insightors_list(self, filters=None):
        allowed_filters = ["country", "specialization", "experience_years", "hourly_rate"]

        if not filters:
            return Insightor.objects.all()
        
        # create a dictionary for query params in allowed_filters
        query_filters = {key: value for key, value in filters.items() if key in allowed_filters}
        return Insightor.objects.filter(**query_filters)
        
