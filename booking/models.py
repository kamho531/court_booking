from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Court(models.Model):
    COURT_CHOICES = [
        ('court_1', 'Court 1'),
        ('court_2', 'Court 2'),
    ]

    name = models.CharField(max_length=20, choices=COURT_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Booking(models.Model):
    GAME_TYPES = [
        ('pickleball', 'Pickleball'),
        ('paddle_ball', 'Paddle Ball'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    game_type = models.CharField(max_length=100, choices=GAME_TYPES)

    def clean(self):
        overlapping_bookings = Booking.objects.filter(
            court = self.court,
            booking_date = self.booking_date,
            start_time__lt = self.end_time,
            end_time__gt = self.start_time,
        ).exclude(id=self.id)

        if overlapping_bookings.exists():
            raise ValidationError('This court is already booked for this time period.')

    def __str__(self):
        return f'{self.user.username} - {self.court} - {self.booking_date} - {self.get_game_type_display()}'
