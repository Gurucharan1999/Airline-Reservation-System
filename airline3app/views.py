from django.shortcuts import render
from airline3app.models import FlightDetail,Route,ForPass,Passengers,Tickets,TicketHolders,NumPrice,DateRoute
from airline3app.forms import SearchForm,UserForm,UserProfileInfoForm,PassengerForm
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from . import models
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
import random
# Create your views here.

global num

@login_required
def index(request):
    form = SearchForm()

    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            return plane_list(request)
        else:
            print("ERROR")

    return render(request,'index.html',{'form':form})


@login_required
def plane_list(request):

    form = SearchForm(request.POST or None)

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            ForPass.objects.all().delete()
            Passengers.objects.all().delete()
            DateRoute.objects.all().delete()
            global num
            num = form.cleaned_data.get('number_of_passengers')
            for i in range(int(num)+1):
                p = ForPass(passenger = i+1)
                p.save()
            p = Route.objects.filter(route_dest = form.cleaned_data.get('destination'),
                                    route_src = form.cleaned_data.get('source'))
            if not p:
                route_id = 1000
            else:
                route_id = p[0].route_no
            flights = FlightDetail.objects.filter(route=route_id)
            dest = form.cleaned_data.get('destination')
            src = form.cleaned_data.get('source')
            q = DateRoute(Route = route_id,Date=form.cleaned_data.get('Date'))
            q.save()
    return render(request, 'plane_list.html', {'form': form,'flights': flights,'dest':dest,'src':src})


def plane_detail_book(request,pk):
    NumPrice.objects.all().delete()
    flights = FlightDetail.objects.filter(pk=pk)
    r = NumPrice(flight_no=flights[0].flight_no,price=flights[0].price)
    r.save()
    return render(request, 'flightdetail.html',{'flights': flights})


def ticket_list(request):
    tickets = Tickets.objects.filter(username=request.user)
    return render(request,'ticket_list.html',{'ticket':tickets})


def my_tickets(request, pk):
    ticket = Tickets.objects.filter(pk=pk)
    object= ticket[0].PNR
    passenger = TicketHolders.objects.filter(PNR = object)
    return render(request, 'my_tickets.html',{'ticket': ticket,'passenger':passenger})


def passenger_info(request):
    global num
    numb = int(num)
    count = ForPass.objects.all().count() - 1
    h = ForPass.objects.order_by('passenger')
    id = h[0].passenger
    ForPass.objects.filter(passenger=id).delete()
    numb = numb+1 - count
    if request.method == "POST" and count>0:
        passenger_details = PassengerForm(data=request.POST)
        if passenger_details.is_valid():
            profile = passenger_details.save(commit=False)
            profile.username = request.user
            profile.save()
            passenger_details = PassengerForm()
        return render(request,'passenger_info.html',{'passenger_details':passenger_details,'count':count,'num':numb })

    elif request.method == "POST" and count==0:
        passenger_details = PassengerForm(data=request.POST)
        if passenger_details.is_valid():
            profile = passenger_details.save(commit=False)
            profile.username = request.user
            profile.save()
        return HttpResponseRedirect(reverse('payments_page'))

    else:
        passenger_details = PassengerForm()

    return render(request,'passenger_info.html',{'passenger_details':passenger_details,'count':count,'num':numb })



def base(request):
    return render(request, 'base.html')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True

        else:
            print("ERROR")
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'register.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('airline3app:user_login'))

def makePNR():
    PNR=''
    while len(PNR)<10:
        n = random.randint(0,9)
        PNR = PNR + str(n)
    k=int(PNR)
    return k


@login_required
def payments_page(request):
    global num
    numb = int(num)
    dateroute = DateRoute.objects.all()
    date = dateroute[0].Date
    route = dateroute[0].Route
    final = Route.objects.filter(route_no=route)
    numprice = NumPrice.objects.all()
    flight_no = numprice[0].flight_no
    final2 = FlightDetail.objects.filter(flight_no=flight_no,route=route)

    price = numprice[0].price
    t_price = price*numb
    if request.method == "POST":

        while True:
            key = makePNR()
            if not Tickets.objects.filter(PNR=key).exists():
                break
        p = Tickets(username = request.user,PNR = key,Date=date,src=final[0].route_src,dest=final[0].route_dest,arrival=final2[0].arrival,departure=final2[0].departure,flight_no=flight_no,price=t_price)
        p.save()
        count = Passengers.objects.all().count()
        for i in range(count):
            Passenger = Passengers.objects.all()
            firstname= Passenger[i].passenger_firstname
            lastname=Passenger[i].passenger_lastname
            age=Passenger[i].passenger_age
            gender=Passenger[i].passenger_gender
            q = TicketHolders(PNR = key, passenger_firstname= firstname,passenger_lastname=lastname,passenger_age=age,passenger_gender=gender)
            q.save()
        return HttpResponseRedirect(reverse('congrats'))

    return render(request,'payments_page.html',{'price':t_price})

@login_required
def congrats(request):

    return render(request,'congrats.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            messages.error(request,'Username or Password not correct! Try Again!')
            return render(request, 'login.html',{})
            #return HttpResponse("Invalid Login Details")
    else:
        return render(request, 'login.html',{})
