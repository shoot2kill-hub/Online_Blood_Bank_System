from django.db import models


# Create your models here.


class Hospital_service(models.Model):
    hospital_name = models.CharField(max_length=100)
    hospital_location = models.CharField(max_length=100)
    hospital_start_time = models.CharField(max_length=250)
    hospital_end_time = models.CharField(max_length=250)
    hospital_date_donating = models.CharField(blank=True, null=True, max_length=250)
    hospital_phone = models.CharField(max_length=250, default='0788101020')
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hospital_name}"

    class Meta:
        verbose_name_plural = " Hospital service"
        ordering = ['-post_date']
