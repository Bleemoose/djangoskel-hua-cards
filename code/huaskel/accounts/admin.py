from django.contrib import admin
from .models import Token, User
# Register your models here.
class UserAdmin(admin.ModelAdmin):

    search_fields = ["id", "first_name", "last_name", "email", "department", "title"]



admin.site.register(Token)
admin.site.register(User,UserAdmin)
