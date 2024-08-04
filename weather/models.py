from django.db import models
from uuid import uuid4

# Create your models here.

class User(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4())
    progress = models.FloatField(default=0.0)
    json = models.TextField(default="")
    date = models.DateTimeField()
