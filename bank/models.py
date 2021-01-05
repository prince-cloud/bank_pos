from django.db import models

from django.contrib.auth.models import User
import datetime
from django.urls import reverse
# Create your models here.
ACCOUNT_CHOICES = (
    ("Susu Banking", "Susu Banking"),
    ("Current Account", "Current Account"),
    ("Fixed Deposite", "Fixed Deposite"),
)
SEX_CHOICES = (
    ("M", "M"),
    ("F", "F"),
)
ID_CHOICES = (
    ("Voters ID","Voters ID"),
    ("Ghana Card","Ghana Card"),
    ("NHIS","NHIS"),
    ("Passport","Passpord"),
    ("Drivers Licensed","Drivers Licensed"),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(upload_to=("profile_image/"), null=True, blank=True)
    digital_address = models.CharField(max_length=12)
    sex = models.CharField(choices=SEX_CHOICES, max_length=2)
    dob = models.DateField()

    next_of_kin = models.CharField(max_length=100, null=True, blank=True)
    next_of_kin_phone_number = models.CharField(max_length=10, null=True, blank=True)
    next_of_kin_digital_address = models.CharField(max_length=12, null=True, blank=True)

    id_type = models.CharField(choices=ID_CHOICES, max_length=50)
    id_number = models.PositiveIntegerField()

    account_number = models.CharField(max_length=10)
    account_type = models.CharField(choices=ACCOUNT_CHOICES,  max_length=100)
    account_balance = models.FloatField()
    
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)

    def get_absolute_url(self) -> str:
        return reverse("bank:profile", kwargs={"pk": self.user.pk})

class Deposite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)

    def save(self, *args, **kwargs):
        self.user.profile.account_balance +=  float(self.amount)
        self.user.profile.save()
        super(Deposite, self).save(*args, **kwargs)


class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)
        
    def save(self, *args, **kwargs):
        self.user.profile.account_balance -=  float(self.amount)
        self.user.profile.save()
        super(Withdrawal, self).save(*args, **kwargs)
