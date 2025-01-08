from django import forms
from .models import Booking
from datetime import time


# Define time choices in 30-minute intervals from 8:00am to 6:00pm
TIME_CHOICES = [
    ('', '------------')
] + [
    (time(hour, minute).strftime('%H:%M'), time(hour, minute).strftime('%I:%M %p'))
    for hour in range(8, 18) for minute in (0, 30)
]

# Add the final time slot of 6:00pm
TIME_CHOICES.append((time(18, 0).strftime('%H:%M'), time(18, 0).strftime('%I:%M %p')))

class BookingForm(forms.ModelForm):

    start_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select(attrs={'class': 'form-control time-input'}))
    end_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select(attrs={'class': 'form-control time-input'}))    
    
    class Meta:
        model = Booking
        fields = ['court', 'booking_date', 'start_time', 'end_time', 'game_type']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control date-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        # if self.user:
        #     self.fields['user'].initial = self.user

    def save(self, commit=True):
        booking = super(BookingForm, self).save(commit=False)
        if self.user:
            booking.user = self.user
        if commit:
            booking.save()
        return booking
