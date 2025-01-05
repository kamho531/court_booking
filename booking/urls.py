from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_court, name='book_court'),
    path('success/', views.booking_success, name='booking_success'),
    path('calendar/', views.booking_calendar, name='booking_calendar'),

]


