from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=100)
    semester = models.IntegerField()

    def __str__(self):
        return self.name
