from django.contrib import admin
from ops.models import *


class ServiceVehicleInline(admin.StackedInline):
    model = ServiceVehicle
    extra = 0

class ServiceAffectedInline(admin.StackedInline):
    model = ServiceAffected
    extra = 0

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time', 'service_type', 'description', 'location')
    list_display_links = ('id','date', 'time', 'service_type', 'description', 'location')
    list_filter = ('service_type',)
    inlines = (ServiceVehicleInline,)

def approve_ops(modeladmin, request, queryset):
    queryset.update(approved_by_ops=True)

def approve_inspector(modeladmin, request, queryset):
    queryset.update(approved_by_inspector=True)


approve_ops.short_description = "Aprobar por operaciones seleccionados"
approve_inspector.short_description = "Aprobar por inspector seleccionados"

class ArrestAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'arrested', 'created_by','was_notified', 'time', 'minutes',  'approved_by_ops','approved_by_inspector')
    list_display_links = ('date', 'description')
    list_filter = ('approved_by_ops','was_notified', 'arrested')
    actions = [approve_ops, approve_inspector]

class ArrestPaymentAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'payer', 'created_by', 'minutes', 'approved_by_ops')
    list_display_links = ('start_time', 'end_time')
    list_filter = ('approved_by_ops','payer')
    actions = [approve_ops]


admin.site.register(Vehicle)
admin.site.register(ServiceAffected)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Arrest, ArrestAdmin)
admin.site.register(ArrestPayment, ArrestPaymentAdmin)

