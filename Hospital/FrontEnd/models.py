from django.db import models
import datetime

# Create your models here.

class DoctorDB(models.Model):
    Name = models.CharField(max_length=100,null=True,blank=True)
    User = models.CharField(max_length=100,null=True,blank=True) #hospital username
    Email = models.CharField(max_length=100,null=True,blank=True)
    Mobile = models.IntegerField(null=True,blank=True)
    Hospital = models.CharField(max_length=100,null=True,blank=True)
    Date = models.DateTimeField(null=True,blank=True)
    Country = models.CharField(max_length=100,null=True,blank=True)
    Specialization = models.CharField(max_length=100,null=True,blank=True)
    Medicalid = models.CharField(max_length=100,null=True,blank=True)
    Username = models.CharField(max_length=100,null=True,blank=True,unique=True)
    Password = models.CharField(max_length=100,null=True,blank=True)
    Medical = models.ImageField(upload_to="MedicalID",null=True,blank=True)
    Photo = models.ImageField(upload_to="profile_pic/doctor",null=True,blank=True)


class HospitalNewDB(models.Model):
    Name = models.CharField(max_length=100,null=True,blank=True)
    Email = models.CharField(max_length=100,null=True,blank=True)
    Mobile = models.IntegerField(null=True,blank=True)
    Address = models.CharField(max_length=100,null=True,blank=True)
    Country = models.CharField(max_length=100,null=True,blank=True)
    H_Username = models.CharField(max_length=100,null=True,blank=True,unique=True)
    H_Password = models.CharField(max_length=100,null=True,blank=True)
    Img = models.ImageField(upload_to="profile_pic/hospital",null=True,blank=True)

class MedicineDB(models.Model):
    Medicine = models.CharField(max_length=100, null=True, blank=True)
    Username = models.CharField(max_length=100, null=True, blank=True)
    Hospital_Name = models.CharField(max_length=100, null=True, blank=True)
    Doctor_User = models.CharField(max_length=100, null=True, blank=True)
    Doctor_Name = models.CharField(max_length=100, null=True, blank=True)
    Morning = models.CharField(max_length=100, null=True, blank=True)
    Afternoon = models.CharField(max_length=100, null=True, blank=True)
    Night = models.CharField(max_length=100, null=True, blank=True)
    Day = models.IntegerField(null=True, blank=True)
    Message = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True,blank=True)


class PatientDB(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=10,null=True,blank=True)
    LName = models.CharField(max_length=10,null=True,blank=True)
    Username = models.CharField(max_length=10,blank=True,unique=True)
    Password = models.CharField(max_length=10,null=True,blank=True)
    Gender = models.CharField(max_length=10,null=True,blank=True)
    Address = models.CharField(max_length=10,null=True,blank=True)
    Mobile = models.IntegerField(null=True,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/Patient/', null=True, blank=True)


class PatientDetailsDB(models.Model):
    Medicine = models.CharField(max_length=100, null=True, blank=True)
    Username = models.CharField(max_length=100, null=True, blank=True)
    Hospital_Name = models.CharField(max_length=100, null=True, blank=True)
    Doctor_User = models.CharField(max_length=100, null=True, blank=True)
    Doctor_Name = models.CharField(max_length=100, null=True, blank=True)
    Morning = models.CharField(max_length=100, null=True, blank=True)
    Afternoon = models.CharField(max_length=100, null=True, blank=True)
    Night = models.CharField(max_length=100, null=True, blank=True)
    Day = models.IntegerField(null=True, blank=True)
    Message = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True,blank=True)

class LabPrescriptionDB(models.Model):
    Message = models.CharField(max_length=100, null=True, blank=True)
    Username = models.CharField(max_length=100, null=True, blank=True)
    Hospital_Name = models.CharField(max_length=100, null=True, blank=True)
    Doctor_Name = models.CharField(max_length=100, null=True, blank=True)
    Doctor_User = models.CharField(max_length=100, null=True, blank=True)
    date=models.DateTimeField(null=True,blank=True)

class LabPrescriptionHistoryDB(models.Model):
    Message = models.CharField(max_length=200, null=True, blank=True)
    Username = models.CharField(max_length=100, null=True, blank=True)
    Hospital_Name = models.CharField(max_length=100, null=True, blank=True)
    Doctor_User = models.CharField(max_length=100, null=True, blank=True)
    Status = models.CharField(max_length=20,default="Pending")
    Report = models.FileField(upload_to='Report',default="Pending")
    lab = models.FileField(max_length=100,default="Pending")
    date=models.DateTimeField(null=True,blank=True)

class LabReportsDB(models.Model):
    Report = models.FileField(upload_to='Report', null=True, blank=True)
    P_Username = models.CharField(max_length=100, null=True, blank=True)
    Hospital_Name = models.CharField(max_length=100, null=True, blank=True)
    Hospital_UserName = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True,blank=True)

class ContactDB(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    Subject = models.CharField(max_length=100, null=True, blank=True)
    Message = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True,blank=True)
