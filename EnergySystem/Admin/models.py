from django.db import models

# Create your models here.
class KSEBOffice(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    office_code = models.CharField(max_length=20, unique=True)
    password=models.CharField(max_length=26)


    def __str__(self):
        return self.name


class ElectricityConsumer(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    connection_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    office_id=models.ForeignKey(KSEBOffice,on_delete=models.CASCADE)
    connection_date = models.DateField(auto_now_add=True)
    status=models.IntegerField()
    lastupdate=models.DateTimeField(auto_now=True)
    password=models.CharField(max_length=26)
    def __str__(self):
        return self.name


class Feedback(models.Model):
    user=models.ForeignKey(ElectricityConsumer,on_delete=models.CASCADE)
    authority=models.IntegerField()###  Admin --> 1 or office -->2
    msg=models.CharField(max_length=250) 
    view_sts=models.IntegerField() #### opposite side viewed or not
    direction=models.IntegerField() ### admin or office --> user stats is 1 and user --> admin or office sts is 2


class Annoucement(models.Model):
    office=models.ForeignKey(KSEBOffice,on_delete=models.CASCADE)
    msg=models.CharField(max_length=250) 
    
class Bill(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(ElectricityConsumer,on_delete=models.CASCADE)
    kwh=models.CharField(max_length=25)
    rate=models.FloatField()
    month=models.CharField(max_length=25)
    BillGenerationdate = models.DateField(auto_now_add=True)
    paymentDate=models.DateTimeField(auto_now=True,blank=True)
    file=models.FileField(upload_to ='uploads/bills', blank=True)
    status=models.IntegerField()

