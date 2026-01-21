from django.db import models

class Student(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.fullname

