from django.db import models
from django.conf import settings
from django.db.models.fields import CharField, TextField

class Note(models.Model):
    title = CharField(max_length=100)
    note = TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    modified_time = models.TimeField(auto_now=True)
