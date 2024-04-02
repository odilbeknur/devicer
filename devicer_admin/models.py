from django.db import models

# Create your models here.

class Responsible(models.Model):
    fullname = models.CharField(max_length=100)
    username = models.TextField(null=True)
    department = models.TextField(null=True)
    position = models.TextField(null=True)
    image = models.ImageField(upload_to='static/images', null=True)

    def __str__(self) -> str:
        return self.fullname
        
class Type(models.Model):
    responsible_id = models.ForeignKey(Responsible, on_delete=models.PROTECT)
    access_choices = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    ]
    access = models.CharField(max_length=10, choices=access_choices)

    def __str__(self) -> str:
        return self.access