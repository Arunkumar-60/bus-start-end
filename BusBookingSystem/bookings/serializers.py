from rest_framework import serializers
from .models import Booking, Bus, Station, RoutePricing

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class RoutePricingSerializer(serializers.ModelSerializer):
    start_station = StationSerializer()
    end_station = StationSerializer()

    class Meta:
        model = RoutePricing
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    starting_station = StationSerializer()
    ending_station = StationSerializer()

    class Meta:
        model = Bus
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
