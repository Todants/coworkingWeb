from django.db import models


class Users(models.Model):
    email = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=50, blank=False)
    date_of_birth = models.DateField(null=False)

    def __str__(self):
        return self.first_name
