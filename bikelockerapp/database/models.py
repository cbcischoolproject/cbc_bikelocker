from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from datetime import date, timedelta
from django.db.models import signals


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField('Location Name', max_length=100)
    location_zip = models.CharField('Location Zip', max_length=10, blank=True)
    location_capacity = models.IntegerField('Location Capacity', default=0)

    class Meta:
        ordering = ['location_name']

    def __str__(self):
        return self.location_name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    def get_location_occ(self):
        return len(Cust_Locker.objects.filter(locker_id__location_id=self.pk))

    def get_renewal_count(self):
        location = Cust_Locker.objects.filter(locker_id__location_id=self.pk).filter(
            cust_id__status_id__status_name__iexact="Active")
        if location:
            return len(location)
        else:
            return 0

    def get_not_renewed_count(self):
        location = Cust_Locker.objects.filter(locker_id__location_id=self.pk).filter(
            cust_id__status_id__status_name__iexact="Not Renewing")
        if location:
            return len(location)
        else:
            return 0

    def get_not_responded(self):
        location = Cust_Locker.objects.filter(locker_id__location_id=self.pk).filter(
            cust_id__status_id__status_name__iexact="Not Responded")
        if location:
            return len(location)
        else:
            return 0

    def get_renewal_percentage(self):
        location = Cust_Locker.objects.filter(locker_id__location_id=self.pk)
        if location:
            location_not_responded = Cust_Locker.objects.filter(locker_id__location_id=self.pk).filter(
                cust_id__status_id__status_name__iexact="Not Responded")
            location_renewed = Cust_Locker.objects.filter(locker_id__location_id=self.pk).filter(
                cust_id__status_id__status_name__iexact="Active")
            location_not_renew = Cust_Locker.objects.filter(locker_id__location_id=self.pk).filter(
                cust_id__status_id__status_name__iexact="Not Renewing")
            if (len(location) > 0):
                top = (len(location_not_renew) + len(location_renewed))
                bottom = (len(location_not_responded) + len(location_renewed) + len(location_not_renew))
                return "{}{}".format(top / bottom * 100, "%")
        return "{}{}".format(0, "%")

class Location_Renewals(models.Model):
    location_renew_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField('Locker Location Renewal Date', null=True)

    def __str__(self):
        return "{} / {}".format(str(self.location), str(self.date))

    class Meta:
        verbose_name = "Locker Location Renewal Date"
        verbose_name_plural = "Locker Location Renewal Dates"
        ordering = ['location']

class Locker_Status(models.Model):
    locker_status_id = models.AutoField(primary_key=True)
    locker_status_name = models.CharField('Locker Status Name', max_length=100)

    def __str__(self):
        return self.locker_status_name

    class Meta:
        verbose_name = "Locker Status"
        verbose_name_plural = "Locker Statuses"

class Locker(models.Model):
    locker_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    locker_name = models.CharField('Locker Name', max_length=100)
    locker_status_id = models.ForeignKey(Locker_Status, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.location_id.location_name + " #" + self.locker_name

    def my_property(self):
        return self.location_id.location_name + " #" + self.locker_name

    locker_name_full = property(my_property)

    class Meta:
        ordering = ['location_id', 'locker_name']

class Maintenance_Type(models.Model):
    main_type_id = models.AutoField('Maintenance Type', primary_key=True)
    main_type_name = models.CharField('Maintenance Type Name', max_length=100)
    main_type_desc = models.CharField('Maintenance Type Description', max_length=100)

    class Meta:
        verbose_name = "Maintenance Type"
        verbose_name_plural = "Maintenance Types"

    def __str__(self):
        return self.main_type_name

    def __unicode__(self):
        return self.main_type_name

class Maintenance_Status(models.Model):
    main_status_id = models.AutoField(primary_key=True)
    main_status_name = models.CharField('Maintenance Status Name', max_length=100)

    def __str__(self):
        return self.main_status_name

    class Meta:
        verbose_name = "Maintenance Status"
        verbose_name_plural = "Maintenance Statuses"

class Maintenance(models.Model):
    SCOPE = (
        ('General Facility', "General Facility"),
        ('Specific Locker(s)', "Specific Locker(s)"),
    )

    maintenance_id = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    main_type_id = models.ForeignKey(Maintenance_Type, on_delete=models.CASCADE)
    maintenance_scope = models.CharField('Maintenance Scope', choices=SCOPE, max_length=50)
    lockers = models.ManyToManyField(Locker, blank=True)
    maintenance_description = models.CharField('Maintenance Description', max_length=250, default='')
    start_date = models.DateField()
    end_date = models.DateField(default=None, blank=True, null=True)
    main_status_id = models.ForeignKey(Maintenance_Status, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return str(self.start_date) + " " + self.location_id.location_name + " - " + self.main_type_id.main_type_name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField('Status Name', max_length=100)
    status_desc = models.CharField('Status Description', max_length=100, blank=True)

    def __str__(self):
        return self.status_name

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    cust_f_name = models.CharField('First Name', max_length=50)
    cust_l_name = models.CharField('Last Name', max_length=50)
    cust_email = models.EmailField('Email', max_length=100, default='')
    cust_phone = models.CharField('Phone #1', max_length=50, default='')
    cust_phone2 = models.CharField('Phone #2', max_length=50, default='', blank=True)
    cust_address = models.CharField('Street Address', max_length=50, default='')
    cust_city = models.CharField('City', max_length=50)
    cust_state = models.CharField('State', max_length=50)
    cust_zip = models.CharField('Zip Code', max_length=10)
    renewed = Status.objects.filter(status_name__iexact="Active")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)

    def not_responded(self):
        if self.status == Status.objects.get(pk=2):
            return True

    def phone_number(self):
        if self.cust_phone:
            first = self.cust_phone[0:3]
            second = self.cust_phone[3:6]
            third = self.cust_phone[6:10]
            return '(' + first + ')' + ' ' + second + '-' + third
        else:
            return 'N/A'

    def phone_number2(self):
        if self.cust_phone2:
            first = self.cust_phone2[0:3]
            second = self.cust_phone2[3:6]
            third = self.cust_phone2[6:10]
            return '(' + first + ')' + ' ' + second + '-' + third
        else:
            return 'N/A'

    def __str__(self):
        return self.cust_f_name + " " + self.cust_l_name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    class Meta:
        ordering = ['cust_l_name']

def delete_inactive_cust_locker(sender, instance, created, **kwargs):
    try:
        cust_locker = Cust_Locker.objects.get(cust_id=instance.cust_id)
        instance_status = instance.status.status_name
        if instance_status == "Inactive":
            cust_locker.delete()
    except:
        inquiry = None

signals.post_save.connect(receiver=delete_inactive_cust_locker, sender=Customer)

class Cust_Status(models.Model):
    cust_status_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    cust_status_date = models.DateField()

    class Meta:
        verbose_name = "Customer Status"
        verbose_name_plural = "Customer Statuses"

class Cust_Locker(models.Model):
    cust_lock_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    locker_id = models.ForeignKey(Locker, on_delete=models.CASCADE)
    contract_date = models.DateField()
    location_renewal = models.ForeignKey(Location_Renewals, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=100, default="", blank=True)
    CONTACT_CHOICES = (
        ('No Contact', 'No Contact'),
        ('Initial Contact', 'Initial Contact'),
        ('Second Contact', 'Second Contact')
    )
    contacted = models.CharField('Contacted', choices=CONTACT_CHOICES, max_length=50, default='No')
    # Couldn't drop this field due to SQLITE3. Now used for renew_dates is now used for locker notes.
    renew_date = models.TextField("Notes", null=True, blank=True, default="")

    @property
    def natural_key(self):
        return self.my_natural_key

    @property
    def total_lockers(self):
        return Locker.objects.count()

    @property
    def is_past_due(self):
        try:
            if self.location_renewal.date:
                return date.today() > self.location_renewal.date
        except:
            return False

    @property
    def is_under_2_weeks_past_due(self):
        try:
            if self.location_renewal.date:
                if (date.today() > self.location_renewal.date and date.today() - timedelta(
                        14) < self.location_renewal.date):
                    return True
        except:
            return False

    @property
    def is_under_2_weeks_not_contacted(self):
        try:
            if self.location_renewal.date:
                if (date.today() > self.location_renewal.date and date.today() - timedelta(
                        14) < self.location_renewal.date):
                            if (date.today() - timedelta(14) > self.location_renewal.date):
                                return True
        except:
            return False

    @property
    def is_2_weeks_past_due(self):
        try:
            if (date.today() - timedelta(14) > self.location_renewal.date):
                return True
        except:
            return False

    @property
    def not_contacted(self):
        if self.contacted == "No Contact":
            return True
        else:
            return False

    @property
    def contacted_once(self):
        if self.contacted == "Initial Contact":
            return True
        else:
            return False

    class Meta:
        verbose_name = "Customer Locker"
        verbose_name_plural = "Customer Lockers"

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    def __str__(self):
        return str(self.cust_id) + " " + str(self.locker_id.location_id) + " #" + self.locker_id.locker_name

    def cust_email(self):
        return self.cust_id.cust_email

    locker_cust_email = property(cust_email)

def create_cust_locker(sender, instance, created, **kwargs):
    try:
        inquiry = Inquiry.objects.get(cust_id=instance.cust_id)
        inquiry.delete()
        locker_leased = Locker_Status.objects.get(locker_status_name='Leased')
        print("locker Status Correct:", locker_leased.pk)
        print("no PK", locker_leased)
        locker = Locker.objects.filter(locker_id=instance.locker_id.pk)
        print("Locker:", locker)
        print("Pre-SaveLocker status:", locker.locker_status_id.locker_status_name)
        print("Pre-Save Locker Status ID:", locker.locker_status_id.locker_status_id)
        locker.locker_status_id.locker_status_id.locker_status_id = locker_leased
        locker.update(locker_status_id=locker_leased)
        print("Post save locker status:", locker.locker_status_id.locker_status_name)
        print("POST-Save Locker Status ID:", locker.locker_status_id.locker_status_id)
    except:
        inquiry = None

signals.post_save.connect(receiver=create_cust_locker, sender=Cust_Locker)

class Inquiry(models.Model):
    inquiry_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inquiry_date = models.DateField()
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"
        ordering = ['inquiry_date']

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    def __str__(self):
        return str(self.cust_id) + " (" + str(self.inquiry_date) + ")"

    def my_property(self):
        return str(self.cust_id)

    customer = property(my_property)
