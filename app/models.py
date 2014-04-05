from django.db import models

class UserInfo(models.Model):
    message = models.CharField(max_length=200)
