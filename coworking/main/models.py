from django.db import models


class Users(models.Model):

    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=False)
    img = models.ImageField(upload_to='upldfile/', default='upldfile/base_avatar.jpg')


class Businesses(models.Model):

    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=50)
    img = models.ImageField(upload_to='upldfile/', default='upldfile/base_avatar.jpg')

    def __str__(self):
        return f'{self.company_name}, {self.email}, {self.password}, {self.phone_number}'


class CoworkingSpaces(models.Model):

    id = models.AutoField(primary_key=True)
    id_company = models.ForeignKey(Businesses, on_delete=models.CASCADE, to_field='id')
    coworking_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=False, null=False)
    date_start = models.TimeField(null=False, default='10:00:00')
    date_end = models.TimeField(null=False, default='22:00:00')
    rating_count = models.BigIntegerField(null=False, default=0)
    rating_sum = models.BigIntegerField(null=False, default=0)
    address = models.CharField(max_length=500, blank=False, null=True)
    benefits = models.JSONField(default={'wifi': False, 'coffe': False, 'printer': False, 'kitchen': False,
                                         'fitness': False, 'fruits': False, 'locker': False, 'parking': False})


class Images(models.Model):

    id = models.AutoField(primary_key=True)
    id_coworking = models.ForeignKey(CoworkingSpaces, on_delete=models.CASCADE, to_field='id')
    file = models.FileField(upload_to='upldfile/')

    def __str__(self):
        return f'{self.id}, {self.id_coworking}, {self.file} '


class Bookings(models.Model):

    id = models.AutoField(primary_key=True)
    id_coworking = models.ForeignKey(CoworkingSpaces, on_delete=models.CASCADE, to_field='id')
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='id')
    price = models.BigIntegerField(null=False)
    type = models.CharField(max_length=50, blank=False, null=False)
    date_start = models.DateTimeField(null=False)
    date_end = models.DateTimeField(null=False)
    rating = models.BigIntegerField(null=False, default=0)


class Services(models.Model):

    id = models.AutoField(primary_key=True)
    id_coworking = models.ForeignKey(CoworkingSpaces, on_delete=models.CASCADE, to_field='id')
    price = models.BigIntegerField(null=False)
    type = models.CharField(max_length=100, blank=False, null=False)
    num_of_seats = models.BigIntegerField(null=False)
    img = models.ImageField(max_length=200, upload_to='upldfile/', null=False, blank=True,
                            default='static/main/img/coworking1.jpg')
