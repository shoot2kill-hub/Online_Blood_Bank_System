from django.db import models
from patient import models as pmodels
from donor import models as dmodels


class Stock(models.Model):
    bloodgroup = models.CharField(max_length=10)
    unit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.bloodgroup


class BloodRequest(models.Model):
    request_by_patient = models.ForeignKey(pmodels.Patient, null=True, on_delete=models.CASCADE)
    request_by_donor = models.ForeignKey(dmodels.Donor, null=True, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=30)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    reason = models.CharField(max_length=500)
    bloodgroup = models.CharField(max_length=10)
    unit = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="Pending")
    date = models.DateField(auto_now=True)


    def __str__(self):
        return self.bloodgroup
