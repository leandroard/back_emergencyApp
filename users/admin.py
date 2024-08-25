from django.contrib import admin
from .models import User, EmergencyRoleModel, Role
from django.utils.translation import gettext_lazy as _




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(EmergencyRoleModel)
class EmergencyRoleModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_requested_role', 'status', 'number_id', 'plate_vehicle')
    list_filter = ('status', 'requested_role')
    search_fields = ('user__email', 'number_id', 'plate_vehicle')
    actions = ['approve_requests', 'reject_requests']

    def get_requested_role(self, obj):
        return obj.requested_role.name
    get_requested_role.short_description = 'Requested Role'

    def approve_requests(self, request, queryset):
        approved_count = 0
        for emergency_role in queryset:
            if EmergencyRoleModel.approve_request(emergency_role.id):
                approved_count += 1
        self.message_user(request, _(f"{approved_count} requests have been approved."))
    approve_requests.short_description = _("Approve selected role change requests")

    def reject_requests(self, request, queryset):
        rejected_count = 0
        for emergency_role in queryset:
            if EmergencyRoleModel.reject_request(emergency_role.id):
                rejected_count += 1
        self.message_user(request, _(f"{rejected_count} requests have been rejected."))
    reject_requests.short_description = _("Reject selected role change requests")



@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass