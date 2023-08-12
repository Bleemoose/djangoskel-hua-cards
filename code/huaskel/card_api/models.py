from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User


class Card(models.Model):
    physical_card_id = models.CharField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_full_name = models.CharField(max_length=200, null=True, blank=True)
    last_check_in = models.DateTimeField(auto_now=True)
    times_checked_in = models.IntegerField(default=0)

    def __str__(self):
        owner = "No owner assigned"
        if self.owner:
            owner = self.owner_full_name
        return "Card " + str(self.id) + " (" + owner + ")"

    def save(self, *args, **kwargs):
        self.set_default_price()
        super(Card, self).save(*args, **kwargs)

    def set_default_price(self):
        if self.owner:
            self.owner_full_name = User.objects.get(pk=self.owner.id).first_name + " " + User.objects.get(
                pk=self.owner.id).last_name
        else:
            self.owner_full_name = "Dont touch C:"


class Station(models.Model):
    station_address = models.CharField(max_length=200)
    last_used = models.DateTimeField(blank=True, null=True)
    is_waiting_for_pair = models.BooleanField(default=False)
    card_to_pair_with = models.ForeignKey(Card, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        address = "No owner assigned"
        if self.station_address:
            address = self.station_address
        return "Station " + str(self.id) + " (" + address + ")"


class CardRegistries(models.Model):
    timestamp = models.DateTimeField(auto_created=True, auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    is_checkout = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) + " Card Registry from: " + str(self.card) + " at: " + self.timestamp.__str__()
    class Meta:
        verbose_name_plural = "CardRegistries"

