from django.db import models
from django.contrib.auth.models import User



class Student(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    level = models.CharField(max_length=5, choices=[('A1',"A1"),('A2',"A2"),('B1',"B1"),('B2',"B2"), ('C1',"C1"),('C2',"C2")], default='A1')
    last_login = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank= True)
    
    def __str__(self):
        return self.full_name

class Interes(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre