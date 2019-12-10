import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Document(models.Model):
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.document
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.uploaded_at <= now
