from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()


# Create your models here.
class Session(models.Model):
    session_id = models.UUIDField(default=uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    expire_date = models.DateTimeField()
