from django.db import models

# Create your models here.

class HospitalDB(models.Model):
    Hosp_Name=models.CharField(max_length=300,null=True,blank=True)
    Location=models.CharField(max_length=300,null=True,blank=True)
    Description=models.CharField(max_length=300,null=True,blank=True)
    Hosp_Image=models.ImageField(upload_to="Hospital Image",null=True,blank=True)

class SpecializationDB(models.Model):
    Specialization = models.CharField(max_length=300,null=True,blank=True)
