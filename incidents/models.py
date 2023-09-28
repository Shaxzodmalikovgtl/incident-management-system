from django.db import models
from django.utils import timezone
from django.utils import timezone
from django.contrib.auth.models import User as DjangoUser
from django.conf import settings
import random


class User(models.Model):
    first_name = models.CharField(max_length=30)  
    last_name = models.CharField(max_length=30)   
    email = models.EmailField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)      
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=20)  
    password = models.CharField(max_length=128)     


    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Incident(models.Model):
    INCIDENT_STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    )
    INCIDENT_PRIORITY_CHOICES = (
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    )

    incident_id = models.CharField(max_length=20, unique=True)
    reporter_id = models.CharField(max_length=20)
    reporter = models.CharField(max_length=40) 
    details = models.TextField()
    reported_datetime = models.DateTimeField(default=timezone.now)
    priority = models.CharField(max_length=10, choices=INCIDENT_PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=15, choices=INCIDENT_STATUS_CHOICES, default='Open')
    is_enterprise = models.BooleanField(default=False)


    def generate_unique_incident_id(self):
        current_year = timezone.now().year
        random_number = random.randint(10000, 99999)
        return f'RMG{random_number}{current_year}'
    
    def save(self, *args, **kwargs):
        if not self.incident_id:
            self.incident_id = self.generate_unique_incident_id()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.incident_id
    