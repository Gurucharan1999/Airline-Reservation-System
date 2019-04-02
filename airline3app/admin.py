from django.contrib import admin
from airline3app.models import Route, FlightDetail, UserTicketRel, PlaneTicketRel, Planes, UserProfileInfo, Tickets

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Route)
admin.site.register(FlightDetail)
admin.site.register(UserTicketRel)
admin.site.register(PlaneTicketRel)
admin.site.register(Tickets)
admin.site.register(Planes)
