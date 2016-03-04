from django.db import models


# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=127, unique=True)
    name = models.CharField(max_length=127,null=True)
    mobile = models.CharField(max_length=13,null=True)
    email = models.CharField(max_length=64,null=True)
    sex = models.CharField(max_length=4,null=True)
    age = models.IntegerField(null=True)
    real_name = models.CharField(max_length=64,null=True)
    id_card = models.CharField(max_length=64,null=True)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    password = models.CharField(max_length=128)
    register_time = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    last_login_ip = models.IPAddressField(null=True)
