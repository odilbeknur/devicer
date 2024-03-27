# rooms/models.py
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    floor = models.IntegerField()
    building = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
