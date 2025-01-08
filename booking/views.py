from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Booking
from .forms import BookingForm
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime



@login_required
def book_court(request):
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Ensure the user is set to the current user
            if booking.court and booking.booking_date and booking.start_time and booking.end_time and booking.game_type:
                try:
                    booking.clean()
                    booking.save()
                    send_booking_confirmation_email(request.user, booking)
                    return redirect('booking_success')
                except ValidationError as e:
                    form.add_error(None, e)
            else:
                message = 'Your booking has failed. Please try again.'
                form.add_error(None, "All fields must be filled out.")
        else:
            message = 'Your booking has failed. Please try again.'
    else:
        form = BookingForm(user=request.user)
        message = ''

    return render(request, 'booking/book_court.html', {'form': form, 'message': message, 'username': request.user.username})


@login_required
def booking_calendar(request):
    bookings = Booking.objects.all()
    events = []
    for booking in bookings:
        events.append({
            'title': f'{booking.court} - {booking.get_game_type_display()}',
            'start': f'{booking.booking_date.isoformat()}T{booking.start_time.isoformat()}',
            'end': f'{booking.booking_date.isoformat()}T{booking.end_time.isoformat()}',
        })
    return render(request, 'booking/booking_calendar.html', {'events': events})



@login_required
def booking_success(request):
    return render(request, 'booking/booking_success.html')


# function to change the time format to 12-hour format in the email
def convert_time_format(time_obj):
    return time_obj.strftime('%I:%M %p')


def send_booking_confirmation_email(user, booking):
    subject = 'Court Booking Confirmation'
    start_time_12hr = convert_time_format(booking.start_time)
    end_time_12hr = convert_time_format(booking.end_time)
    message = f'Dear {user.username},\n\nYour booking has been confirmed.\n\nDetails:\nCourt: {booking.court}\nDate: {booking.booking_date}\nStart Time: {start_time_12hr}\nEnd Time: {end_time_12hr}\nGame Type: {booking.get_game_type_display()}\n\nThank you for your booking!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)




