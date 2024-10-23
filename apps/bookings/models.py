from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField
from datetime import timedelta

from apps.accounts.models import User
from apps.common.models import BaseModel
from apps.profiles.models import Insightor


class Booking(BaseModel):

    BOOKING_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed")
    )

    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "paid")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insightor = models.ForeignKey(Insightor, on_delete=models.CASCADE)
    num_hours = models.IntegerField(default=1)
    subject = models.CharField(max_length=300)
    user_needs = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    scheduled_for = models.DateTimeField()
    time_range= DateTimeRangeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default="pending")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending")
    is_done = models.BooleanField(default=False)

    def save(self, *args, **Kwargs):
        session_end = self.scheduled_for + timedelta(hours=self.num_hours)
        self.time_range = (self.scheduled_for, session_end)
        super().save(*args, **Kwargs)

    def __str__(self):
        return f"{self.scheduled_for} | {self.payment_status} | with {self.user.full_name} on {self.subject})"

    
