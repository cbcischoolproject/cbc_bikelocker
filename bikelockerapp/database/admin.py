from django.contrib import admin

# Register your models here.
from .models import *

class LocationA(admin.ModelAdmin):
    list_display = ('location_name', 'location_zip')
    list_filter = ('location_name', 'location_zip',)

class MaintenanceAdmin(admin.ModelAdmin):
    list_filter = ('main_type_id', 'location_id')

class Location_Renewals_A(admin.ModelAdmin):
    list_display = ('location', 'date')
    list_filter = ('location', 'date',)

class CustomerAdmin:
    list_display = ('cust_f_name', 'cust_l_name', 'cust_email')
    list_filter = ('status')

admin.site.register(Location, LocationA)
admin.site.register(Waitlist)
admin.site.register(Locker_Status)
admin.site.register(Location_Renewals, Location_Renewals_A)
admin.site.register(Locker)
admin.site.register(Key_Status)
admin.site.register(Key)
admin.site.register(Maintenance_Type)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Status)
admin.site.register(Cust_Status)
admin.site.register(Maintenance_Status)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Cust_Locker)
admin.site.register(Renewal)
admin.site.register(Renewal_Response)
admin.site.register(Inquiry)
admin.site.register(Locker_Log)
admin.site.register(Renewal_Form)
admin.site.register(Staff)


