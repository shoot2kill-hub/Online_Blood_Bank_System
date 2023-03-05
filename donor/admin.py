from django.contrib import admin
from donor.models import Donor, BloodDonate, LabResult

# Register your models here.


admin.site.register(Donor)

admin.site.register(BloodDonate)
admin.site.register(LabResult)
