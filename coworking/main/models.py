from django.db import models


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


class Businesses(models.Model):
    objects = models.Manager()

    company_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.company_name} , {self.email} ,{self.password} ,{self.phone_number}'


class CoworkingSpaces(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_company = models.BigIntegerField(null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    date_start = models.TimeField(null=False)
    date_end = models.TimeField(null=False)
    rating = models.FloatField(null=False, default=0)

    def __str__(self):
        return f'{self.id_company} , {self.description} ,{self.date_start} ,{self.date_end}, {self.rating}'


class Images(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_coworking = models.BigIntegerField(null=False)
    file = models.FileField(upload_to='upldfile/')

    def __str__(self):
        return f'{self.id} , {self.id_coworking} ,{self.file} '


class Bookings(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_coworking = models.BigIntegerField(null=False)
    id_user = models.BigIntegerField(null=False)
    price = models.BigIntegerField(null=False)
    type = models.CharField(max_length=50, blank=False, null=False)
    date_start = models.DateTimeField(null=False)
    date_end = models.DateTimeField(null=False)


class Services(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_coworking = models.BigIntegerField(null=False)
    price = models.BigIntegerField(null=False)
    type = models.CharField(max_length=50, blank=False, null=False)
    num_of_seats = models.BigIntegerField(null=True)
    img = models.ImageField(upload_to='upldfile/', null=True, blank=True)
