from django.contrib import admin
from .models import EmergencyType, Emergency


@admin.register(EmergencyType)
class EmergenciesTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Emergency)
class  EmergencyAdmin(admin.ModelAdmin):
    pass