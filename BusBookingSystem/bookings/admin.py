from django.contrib import admin
from .models import Bus, Booking, Station, BusStationTime, RoutePricing

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'bus', 'seat_number', 'is_approved', 'qr_code')
    actions = ['approve_bookings']

    def approve_bookings(self, request, queryset):
        for booking in queryset:
            if not booking.is_approved:
                booking.is_approved = True
                booking.generate_qr_code()
                booking.save()
        self.message_user(request, "Selected bookings approved and QR codes generated.")

admin.site.register(Station)
admin.site.register(Bus)
admin.site.register(BusStationTime)
admin.site.register(RoutePricing)
admin.site.register(Booking, BookingAdmin)
