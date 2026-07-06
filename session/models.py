from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Session(models.Mode):
    session_id = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    expire_date = models.DateTimeField()
