from django.db import models


# Create your models here.
class Session(models.Model):
    session_key = models.CharField(max_length=64, primary_key=True)
    session_data = models.TextField(null=True, blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)
