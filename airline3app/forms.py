from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.models import User
from airline3app.models import UserProfileInfo,Passengers


class SearchForm(forms.Form):
   source = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
   destination = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
   Date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker','autocomplete': 'off'}))
   number_of_passengers = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name','last_name','username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

class PassengerForm(forms.ModelForm):
    class Meta():
        model = Passengers
        fields = (
        'passenger_firstname',
        'passenger_lastname',
        'passenger_age',
        'passenger_gender')
