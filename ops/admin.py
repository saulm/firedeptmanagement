from django.contrib import admin
from ops.models import *


class ServiceVehicleInline(admin.StackedInline):
    model = ServiceVehicle

class ServiceAffectedInline(admin.StackedInline):
    model = ServiceAffected
    extra = 1

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time', 'service_type', 'description', 'location')
    list_display_links = ('id','date', 'time', 'service_type', 'description', 'location')
    list_filter = ('service_type',)
    inlines = (ServiceVehicleInline,)

admin.site.register(Vehicle)
admin.site.register(ServiceAffected)
admin.site.register(Service, ServiceAdmin)
