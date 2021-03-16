from django.db import models
from django.core.validators import MaxValueValidator
#from phonenumber_field.modelfields import PhoneNumberField




class Locations(models.Model):
    pincode = models.IntegerField(primary_key=True)
    zone = models.CharField(max_length=5)
    def __str__(self):
        return str(self.pincode)

class Hospitals(models.Model):
    beds=models.CharField(null=True,max_length=4)
    hosp_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    status = models.CharField(max_length=100)
    pincodes = models.ForeignKey(Locations, default=1, verbose_name="pin", on_delete=models.SET_DEFAULT)

    def __str__(self):
        return str(self.hosp_id)
class Hospital_phones(models.Model):
    sl_no = models.IntegerField(primary_key=True)
    h_id = models.ForeignKey(Hospitals,default=1,verbose_name='hid',on_delete=models.SET_DEFAULT)
    phno = models.BigIntegerField()
    def __str__(self):
        return str(self.h_id)


class At_Risk(models.Model):

    phno=models.CharField(primary_key=True,default='',max_length=10)
    age = models.IntegerField(null = True)
    symptom = models.CharField(max_length=100)
    disease = models.CharField(max_length=100)
    travel=models.CharField(max_length=100)
    apply=models.CharField(max_length=100)
    result=models.CharField(default="low",max_length=100)
    def __str__(self):
        return str(self.phno)

class District(models.Model):

    district_name = models.CharField(max_length=100,primary_key=True)
    total_cases = models.TextField()
    active_cases = models.TextField()
    cured = models.TextField()
    death = models.TextField()
    def __str__(self):
        return str(self.district_name)




class Totalcases(models.Model):

    total_case = models.IntegerField(primary_key=True)
    total_discharged = models.IntegerField()
    total_deaths = models.IntegerField()
    def __str__(self):
        return str(self.total_case)



class State_wise(models.Model):

    state= models.CharField(max_length=100, primary_key=True)
    state_discharged = models.IntegerField()
    state_case=models.IntegerField()
    state_deaths = models.IntegerField()
    def __str__(self):
        return str(self.state_no)
class Self_assess(models.Model):
    phno=models.CharField(max_length=10,default='',primary_key=True)
    age = models.IntegerField()
    symptoms = models.CharField(max_length=100)
    disease = models.CharField(max_length=100)
    travelled = models.CharField(max_length=3)
    applies = models.CharField(max_length=100)
    result = models.CharField(default="Low", max_length=100)
    # no=models.CharField(max_length=10,null=True)
    def __str__(self):
        return str(self.phno)







