from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=30)
    company_address = models.TextField()
    company_bio = models.TextField(blank=True, null=True)
    website = models.URLField()
    contact_number = models.CharField(max_length=10)
    email = models.EmailField()
    type = models.CharField(max_length=15, default='company')

    def __str__(self):
        return self.company_name


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    email = models.EmailField()
    time_date = models.DateTimeField()
    skill = models.CharField(max_length=255)
    job_type = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    type     = models.CharField(max_length=15, default='student')

    def __str__(self):
        return self.username