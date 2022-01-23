from django.db import models
from django.utils import timezone


class Common(models.Model):
    order = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now, null=True, editable=False)
    updated_date = models.DateTimeField(default=timezone.now, null=True)
    deleted_date = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.order
