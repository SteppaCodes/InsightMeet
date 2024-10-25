from django.urls import path
from .views import (
    BookingsListCreateAPIView,
    BookSessionAPIView
)

urlpatterns = [
    path("bookings/", BookingsListCreateAPIView.as_view()),
    path("book-session/", BookSessionAPIView.as_view())
]