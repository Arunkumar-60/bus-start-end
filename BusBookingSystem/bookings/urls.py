from django.urls import path
from .views import book_ticket, approve_booking

urlpatterns = [
    path('book/<int:bus_id>/<int:start_station_id>/<int:end_station_id>/<int:seat_number>/', book_ticket, name='book-ticket'),
    path('approve/<int:booking_id>/', approve_booking, name='approve-booking'),
]
