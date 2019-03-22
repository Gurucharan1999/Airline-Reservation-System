from django.shortcuts import render
from airline3app.models import FlightDetail,Route,ForPass,Passengers
from airline3app.forms import SearchForm,UserForm,UserProfileInfoForm,PassengerForm
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from . import models
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
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
            global num
            num = form.cleaned_data.get('number_of_passengers')
            for i in range(int(num)+1):
                p = ForPass(passenger = i+1)
                p.save()
            p = Route.objects.filter(route_dest = form.cleaned_data.get('destination'),route_src = form.cleaned_data.get('source'))
            if not p:
                route_id = 1000
            else:
                route_id = p[0].route_no
            flights = FlightDetail.objects.filter(route=route_id)

    return render(request, 'plane_list.html', {'form': form,'flights': flights})


class plane_detail_book(DetailView):
    context_object_name = 'flights'
    model = models.FlightDetail
    template_name = 'flightdetail.html'
    def get_context_data(self, **kwargs):
        context = super(plane_detail_book, self).get_context_data(**kwargs)
        context['hello'] = ForPass.objects.all()
        return context

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
        return HttpResponseRedirect(reverse('airline3app:passenger_info'))

    elif request.method == "POST" and count==0:
        passenger_details = PassengerForm(data=request.POST)
        if passenger_details.is_valid():
            profile = passenger_details.save(commit=False)
            profile.username = request.user
            profile.save()
        return HttpResponseRedirect(reverse('index'))

    else:
        passenger_details = PassengerForm()

    return render(request,'passenger_info.html',{'passenger_details':passenger_details,'count':count,'num':numb })



def base(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

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
    return HttpResponseRedirect(reverse('about'))

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
