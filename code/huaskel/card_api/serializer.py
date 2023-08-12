from rest_framework import serializers
from .models import Card, CardRegistries


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'owner_full_name', 'owner_id', 'times_checked_in', 'last_check_in')


class CardRegistriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardRegistries
        fields = ('id', 'timestamp', 'checkin_or_checkout', 'card_id', 'owner_id', 'station_id')
