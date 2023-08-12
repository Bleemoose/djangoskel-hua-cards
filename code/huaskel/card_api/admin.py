from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import *
import csv
from django.http import HttpResponse





# Register your models here.
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def has_module_permission(self, request):
        return True

    search_fields = ["id", "owner_full_name", "owner__username", "owner__email", "owner__department", "owner__id"]

    actions = ["export_as_csv"]

    change_form_template = "my_button.html"

    def response_change(self, request, obj):
        if "_make-pairing" in request.POST:
            station_from_request = request.POST.__getitem__('stations')
            print(station_from_request)
            station = get_object_or_404(Station, id=station_from_request)
            station.is_waiting_for_pair = True
            station.card_to_pair_with = obj
            station.save()

            self.message_user(request, "Station with id: " + str(station.id) + " is waiting for card pairing")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)



@admin.register(CardRegistries)
class CardRegistriesAdmin(admin.ModelAdmin):
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    actions = ["export_as_csv"]

    search_fields = ["id","timestamp","owner__username","owner__first_name","owner__last_name"]

admin.site.register(Station)
