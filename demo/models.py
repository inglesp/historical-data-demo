from django.db import models


class Practice(models.Model):
    release_date = models.DateField()
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("release_date", "code")
