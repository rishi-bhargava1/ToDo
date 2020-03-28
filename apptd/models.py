from django.db import models

# Create your models here.
class register(models.Model):
    iid = models.AutoField(primary_key=True)
    Uname = models.CharField(max_length=20, default="")
    Upaswd = models.IntegerField(default=0)

# class register1(models.Model):
#     Uname = models.CharField(max_length=20, default="")
#     Upaswd = models.IntegerField(default=0)
