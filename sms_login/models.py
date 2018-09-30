from django.db import models


class Users(models.Model):
    phone_number = models.CharField(max_length=15)
    four_digit_code = models.CharField(max_length=4, default="0000")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number


class Tokens(models.Model):
    token = models.CharField(max_length=15)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
