from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Route(models.Model):
    route_no = models.AutoField(primary_key=True)
    route_dest = models.CharField(max_length = 100)
    route_src = models.CharField(max_length = 100)
    class Meta:
        unique_together = (('route_dest', 'route_src'),)

class Planes(models.Model):
    flight_code = models.CharField(max_length = 100, primary_key=True)
    price = models.PositiveIntegerField()

class Tickets(models.Model):
    JDate = models.DateField()
    GENDER_CHOICES = (
        ('male', 'MALE'),
        ('female', 'FEMALE'),
        ('other', 'OTHER'),
    )
    PNR = models.PositiveIntegerField(primary_key=True)
    passenger_firstname = models.CharField(max_length = 100)
    passenger_lastname = models.CharField(max_length = 100)
    passenger_dob = models.DateField()
    passenger_gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='female')
    def get_absolute_url(self):
        return reverse("my_tickets",kwargs={'pk': PNR})

class FlightDetail(models.Model):
    DAYS = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )
    flight_code = models.ForeignKey(Planes, on_delete=models.CASCADE)
    route_no = models.ForeignKey(Route, on_delete=models.CASCADE)
    Day = models.CharField(null=True, choices=DAYS)
    arrival = models.TimeField()
    departure = models.TimeField(null=True)
    def get_absolute_url(self):
        return reverse("plane_detail_book",kwargs={'pk': self.pk})

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    def __str__(self):
        return self.user.username

class UserTicketRel(models.Model):
    username = models.ForeignKey(User, on_delete=models.SET_NULL)
    Date_of_booking = models.DateField()
    PNR = models.ForeignKey(Tickets, on_delete=None)

class PlaneTicketRel(models.Model):
    PNR = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    flight_code = models.ForeignKey(Planes, on_delete=models.CASCADE)