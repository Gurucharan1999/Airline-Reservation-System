from django.contrib import admin
from airline3app.models import Route,FlightDetail,ForPass
from airline3app.models import UserProfileInfo,Passengers,TicketHolders,Tickets

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Route)
admin.site.register(FlightDetail)
admin.site.register(ForPass)
admin.site.register(Passengers)
admin.site.register(Tickets)
admin.site.register(TicketHolders)
