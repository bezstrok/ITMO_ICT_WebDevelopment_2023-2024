from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Car, DriverLicense, Owning

# admin.site.register(Driver)
admin.site.register(Car)
admin.site.register(DriverLicense)
admin.site.register(Owning)


class CustomUserAdmin(UserAdmin):
	fieldsets = UserAdmin.fieldsets + (
		('Custom fields', {'fields': ('passport_number', 'home_address', 'nationality')}),
	)


admin.site.register(get_user_model(), CustomUserAdmin)
