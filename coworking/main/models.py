from django.db import models
from django.contrib.auth.hashers import check_password


class Users(models.Model):
    objects = models.Manager()

    email = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=False)

    def __str__(self):
        return self.first_name

    def check_password(self, password):
        return check_password(password, self.password)


class Businesses(models.Model):
    objects = models.Manager()

    company_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=50)

    def check_password(self, password):
        return check_password(password, self.password)


class CoworkingSpaces(models.Model):
    id_company = models.BigIntegerField(null=False)
    description = models.CharField(max_length=50, blank=False, null=False)
    date_start = models.TimeField(null=False)
    date_end = models.TimeField(null=False)


class Images(models.Model):
    id_coworking = models.BigIntegerField(null=False)
    file = models.FileField(upload_to='upldfile/')


class Bookings(models.Model):
    id_coworking = models.BigIntegerField(null=False)
    id_user = models.BigIntegerField(null=False)
    price = models.BigIntegerField(null=False)
    type = models.CharField(max_length=50, blank=False, null=False)
    date_start = models.DateTimeField(null=False)
    date_end = models.DateTimeField(null=False)


class Services(models.Model):
    id_coworking = models.BigIntegerField(null=False)
    price = models.BigIntegerField(null=False)
    type = models.CharField(max_length=50, blank=False, null=False)
    num_of_seats = models.BigIntegerField(null=True)
