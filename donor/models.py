from django.db import models
from django.contrib.auth.models import User


class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/Donor/', null=True, blank=True)

    email = models.CharField(max_length=40)

    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name




class LabResult(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    hepatitis = models.CharField(max_length=10)
    cancer = models.CharField(max_length=10)
    hiv = models.CharField(max_length=10)
    diabetes = models.CharField(max_length=10)
    malaria = models.CharField(max_length=10)
    approve_blood = models.BooleanField()

    def __str__(self):
        return self.donor.get_name


class BloodDonate(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100, default="Nothing")
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    occupation = models.CharField(max_length=20)
    weight = models.CharField(max_length=10)
    bloodpressure = models.CharField(max_length=10)
    pulse = models.CharField(max_length=10)
    temperature = models.CharField(max_length=10)
    bloodgroup = models.CharField(max_length=10)
    unit = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="Pending")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.donor

    @property
    def getLabResult(self):
        result = None
        try:
            labresult = LabResult.objects.get(donor=self.donor)
            if labresult.approve_blood:
                result = "approved"
            else:
                result = "rejected"
        except:
            result = "pending"
        return result

