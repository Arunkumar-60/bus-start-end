from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO

class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Bus(models.Model):
    bus_number = models.CharField(max_length=10, unique=True)
    starting_station = models.ForeignKey(Station, related_name="starting_buses", on_delete=models.CASCADE)
    ending_station = models.ForeignKey(Station, related_name="ending_buses", on_delete=models.CASCADE)
    stations = models.ManyToManyField(Station, related_name="passing_buses", through="BusStationTime")
    total_seats = models.IntegerField()

    def __str__(self):
        return f"{self.bus_number}: {self.starting_station} ➝ {self.ending_station}"

class BusStationTime(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    def __str__(self):
        return f"{self.bus.bus_number} at {self.station.name} ({self.arrival_time} - {self.departure_time})"

class RoutePricing(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    start_station = models.ForeignKey(Station, related_name="start_routes", on_delete=models.CASCADE)
    end_station = models.ForeignKey(Station, related_name="end_routes", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.start_station} ➝ {self.end_station}: ₹{self.price}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    start_station = models.ForeignKey(Station, related_name="departure_bookings", on_delete=models.CASCADE)
    end_station = models.ForeignKey(Station, related_name="arrival_bookings", on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    payment_status = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"Booking: {self.user.username} - {self.start_station} ➝ {self.end_station} - Seat {self.seat_number}"

    def generate_qr_code(self):
        """Generate QR code only when approved."""
        if self.is_approved:
            qr_data = f"Passenger: {self.user.username}\nBus: {self.bus.bus_number}\nRoute: {self.start_station} ➝ {self.end_station}\nSeat: {self.seat_number}\nPrice: ₹{self.price}"
            qr = qrcode.make(qr_data)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            self.qr_code.save(f"qr_{self.id}.png", ContentFile(buffer.getvalue()), save=False)
