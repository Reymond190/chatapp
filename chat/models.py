from django.contrib.auth.models import User
from django.db import models


class plan(models.Model):
    plan_name= models.CharField(max_length=100,null=True)
    plan_id = models.CharField(max_length=100,unique=True,null=True)
    users = models.CharField(max_length=100,null=True)
    devices = models.IntegerField(null=True)
    expand_upto = models.IntegerField(null=True)
    price = models.FloatField(default=0)
    add = models.FloatField(default=0)
    total_price = models.FloatField(null=True)
    subscription_time = models.DurationField(null=True)
    yearly = models.BooleanField(default=False)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True)