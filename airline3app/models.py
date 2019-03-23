from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

GENDER_CHOICES = (
    ('male','MALE'),
    ('female', 'FEMALE'),
    ('other','OTHER'),
)

class ForPass(models.Model):
    passenger = models.CharField(max_length = 10)

class Route(models.Model):
    route_no = models.CharField(max_length = 10)
    route_dest = models.CharField(max_length = 100)
    route_src = models.CharField(max_length = 100)

class FlightDetail(models.Model):
    flight_no = models.CharField(max_length = 100,)
    route = models.CharField(max_length = 100)

    def get_absolute_url(self):
        return reverse("plane_detail_book",kwargs={'pk': self.pk})

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username

class Passengers(models.Model):
    username = models.ForeignKey(User, null=False, blank=False,on_delete=None)
    passenger_firstname = models.CharField(max_length = 100)
    passenger_lastname = models.CharField(max_length = 100)
    passenger_age = models.PositiveIntegerField()
    passenger_gender =  models.CharField(max_length=6, choices=GENDER_CHOICES, default='female')

class Tickets(models.Model):
    username = models.ForeignKey(User, null=False, blank=False,on_delete=None)
    PNR = models.PositiveIntegerField(unique=True)

    def get_absolute_url(self):
        return reverse("my_tickets",kwargs={'pk': self.pk})


class TicketHolders(models.Model):
    PNR = models.PositiveIntegerField()
    passenger_firstname = models.CharField(max_length = 100)
    passenger_lastname = models.CharField(max_length = 100)
    passenger_age = models.PositiveIntegerField()
    passenger_gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='female')
