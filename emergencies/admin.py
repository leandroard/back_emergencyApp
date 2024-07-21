from django.contrib import admin
from .models import EmergencyType, Emergency


@admin.register(EmergencyType)
class EmergenciesTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' )

@admin.register(Emergency)
class  EmergencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'emergency_type')