from django.contrib import admin

# Register your models here.
from .models import *

# These Admin subclasses add additional filtering features when viewing Models.
class LocationAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('location_name', 'location_zip')
    list_filter = ('location_name', 'location_zip',)

class MaintenanceAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('main_type_id', 'location_id', 'maintenance_description', 'start_date', 'end_date')
    list_filter = ('main_type_id', 'location_id')

class Location_Renewals_Admin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('location', 'date')
    list_filter = ('location', 'date',)

class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('cust_f_name', 'cust_l_name', 'cust_email', 'cust_address', 'cust_city', 'cust_state', 'cust_zip', 'cust_phone', 'status')
    list_filter = ('status', 'cust_city')

class LockerAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('locker_name_full', 'locker_status_id')
    list_filter = ('locker_status_id', 'location_id',)

class Cust_LockerAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('cust_id', 'locker_cust_email', 'locker_id', 'contract_date')
    list_filter = ('locker_id__location_id', 'contract_date')

class InquiryAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('customer', 'inquiry_date')
    list_filter = ('locations', 'inquiry_date')

admin.site.register(Location, LocationAdmin)
admin.site.register(Waitlist)
admin.site.register(Locker_Status)
admin.site.register(Location_Renewals, Location_Renewals_Admin)
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


