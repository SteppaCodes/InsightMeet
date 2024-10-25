from apps.profiles.models import Insightor
from apps.bookings.models import Booking
from apps.accounts.models import User

from datetime import timedelta, datetime

from django.db.models import Exists, OuterRef
from django.utils.timezone import make_aware

def calculate_session_end_plus_break(date_time, session_length):
    session_end = date_time + timedelta(hours=session_length) + timedelta(minutes=30)
    return session_end

def get_available_insightors(date_time:datetime, session_length:int, user:User) -> list[Insightor]:
    """
        This function queries the db for free insightors
    """
    session_end = calculate_session_end_plus_break(date_time, session_length)
    day_of_week = date_time.strftime('%A')

    insightors = Insightor.objects.annotate(
        is_booked= Exists(Booking.objects.filter(
            time_range__overlap=(date_time, session_end),
            insightor=OuterRef("pk"),
            status="confirmed",
        ))
    ).filter(is_booked=False,
            available=True,
            available_days__icontains=day_of_week,
            work_start__lte=date_time.time(),
            work_end__gte=session_end.time()
        ).exclude(user=user)

    if not insightors:
        return None

    return insightors

def is_insightor_available(date_time:datetime, insightor: Insightor, session_length: int) -> bool:
    start_time = date_time
    end_time = calculate_session_end_plus_break(date_time, session_length)

    # Get the name of the day of the week - this would be used to check if the consultant is available for that day
    day_of_week = date_time.strftime("%A")

    is_available = Booking.objects.filter(
        scheduled_for=date_time,
        insightor=insightor,
        status="confirmed",
        time_range__overlap=(start_time, end_time),
        insightor__available_days__icontains=day_of_week,
        insightor__work_start__lte=start_time.time(),
        insightor__work_end__gte=end_time.time()
    ).exists()

    return is_available

def get_available_time_slots(date_time: datetime, insightor: Insightor, session_length: int) -> list[datetime]:
    session_length_delta = timedelta(hours=session_length)
    available_slots = []

    work_start = make_aware(datetime.combine(date_time.date(), insightor.work_start))
    work_end = make_aware(datetime.combine(date_time.date(), insightor.work_end))

    # Get all bookings that have been confirmed i.e paid for
    bookings = Booking.objects.filter(
        insightor=insightor,
        scheduled_for__date= date_time.date(),
        status="confirmed"
    ).only("scheduled_for", "time_range").order_by("scheduled_for")

    # set the current time to the insightor's start of day
    current_time = work_start

    """
        The logic is to calculate time gaps between sessions, and add time gaps that can accomodate
        the session length and doesnt overlap with any session
    """
    for booking in bookings:
        booking_start = booking.scheduled_for
        booking_end = calculate_session_end_plus_break(booking.scheduled_for, booking.num_hours)

        while current_time + session_length_delta < booking_start:
            potential_start = current_time
            potential_end = current_time + session_length_delta

            overlaps = bookings.filter(
                time_range__overlap=(potential_start, potential_end)
            )

            if not overlaps:
                available_slots.append(
                    {
                        "start": potential_start,
                        "end": potential_end
                    }
                )
            current_time = potential_end

        current_time = booking_end

    """ 
        After all bookings, we check the remaining time left to see if they can accomodate a slot of 
        the session length user specified
    """
    while current_time + session_length_delta < work_end:
        potential_start = current_time
        potential_end = potential_start + session_length_delta
                    
        overlaps = bookings.filter(
                    time_range__overlap=(potential_start, potential_end)
                ).exists()

        if not overlaps:
                    available_slots.append({
                        "start": potential_start,
                        "end": potential_end
                    })

        current_time = potential_end


    if not len(available_slots) > 0:
        return None

    return available_slots


