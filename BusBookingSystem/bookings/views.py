from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Bus, Booking, Station, RoutePricing
from .serializers import BookingSerializer, BusSerializer, RoutePricingSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_ticket(request, bus_id, start_station_id, end_station_id, seat_number):
    """User books a ticket (Admin must approve)."""
    user = request.user
    bus = get_object_or_404(Bus, id=bus_id)
    start_station = get_object_or_404(Station, id=start_station_id)
    end_station = get_object_or_404(Station, id=end_station_id)

    # Check if seat is already booked
    if Booking.objects.filter(bus=bus, seat_number=seat_number, is_approved=True).exists():
        return JsonResponse({"error": "Seat already booked"}, status=400)

    if seat_number <= 0:
        return JsonResponse({"error": "Seat number must be a positive integer"}, status=400)

    if seat_number > bus.total_seats:
        return JsonResponse({"error": f"Invalid seat number. Choose between 1 and {bus.total_seats}"}, status=400)


    # Get ticket price
    route_price = RoutePricing.objects.filter(bus=bus, start_station=start_station, end_station=end_station).first()
    if not route_price:
        return JsonResponse({"error": "No price available for this route"}, status=400)

    booking = Booking.objects.create(
        user=user,
        bus=bus,
        start_station=start_station,
        end_station=end_station,
        seat_number=seat_number,
        price=route_price.price,
    )

    return JsonResponse({"message": "Booking request sent. Waiting for admin approval.", "booking_id": booking.id})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_booking(request, booking_id):
    """Admin approves a booking and generates QR code."""
    booking = get_object_or_404(Booking, id=booking_id)
    booking.is_approved = True
    booking.generate_qr_code()
    booking.save()

    return JsonResponse({"message": "Booking approved! QR code generated.", "qr_code_url": booking.qr_code.url})
