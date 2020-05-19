from django.contrib import admin

# Register your models here.
from .models import *

class LocationA(admin.ModelAdmin):
    list_display = ('location_name', 'location_zip')
    list_filter = ('location_name', 'location_zip',)

class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('main_type_id', 'location_id', 'description', 'start_date', 'end_date')
    list_filter = ('main_type_id', 'location_id', 'start_date', 'end_date')

class Location_Renewals_A(admin.ModelAdmin):
    list_display = ('location', 'date')
    list_filter = ('location', 'date',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_f_name', 'cust_l_name', 'cust_email', 'status')
    list_filter = ('status',)

class LockerAdmin(admin.ModelAdmin):
    list_display = ('locker_name_full', 'locker_status_id')
    list_filter = ('locker_status_id', 'location_id',)

class Cust_LockerAdmin(admin.ModelAdmin):
    list_display = ('cust_id', 'locker_id', 'contract_date', 'location_renewal')
    list_filter = ('locker_id__location_id', 'contract_date')

class InquiryAdmin(admin.ModelAdmin):
    list_display = ('inquiry_full', 'inquiry_date')
    list_filter = ('inquiry_date', 'cust_id', 'locations')

admin.site.register(Location, LocationA)
admin.site.register(Waitlist)
admin.site.register(Locker_Status)
admin.site.register(Location_Renewals, Location_Renewals_A)
admin.site.register(Locker, LockerAdmin)
admin.site.register(Key_Status)
admin.site.register(Key)
admin.site.register(Maintenance_Type)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Status)
admin.site.register(Cust_Status)
admin.site.register(Maintenance_Status)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Cust_Locker, Cust_LockerAdmin)
admin.site.register(Renewal)
admin.site.register(Renewal_Response)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(Staff)


