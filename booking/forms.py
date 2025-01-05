from django import forms
from .models import Booking, Court

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['court', 'booking_date', 'start_time', 'end_time', 'game_type']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
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
