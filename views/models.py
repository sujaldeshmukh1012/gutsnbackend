from django.db import models


class IpModel(models.Model):
    ip = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip


