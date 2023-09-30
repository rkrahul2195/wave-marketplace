from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Client, User,Freelencer,ProjectModel

#Freelancer 
class FreelancerSignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=30)
    birth_day = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(max_length=100)
    skill = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username','phone','email','password1','password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_freelencer = True
        if commit:
            user.save()
            freelancer = Freelencer.objects.create(user=user, full_name=self.cleaned_data['full_name'],
                                       birth_day=self.cleaned_data['birth_day'],
                                       email=user.email,phone=self.cleaned_data['phone'],address=self.cleaned_data['address'],
                                       skill=self.cleaned_data['skill'])
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


#Client
class ClientSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    birth_day = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    company = forms.CharField(required=True)
    profession = forms.CharField(required=True)
    address = forms.CharField(max_length=100)
    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_client = True
        if commit:
            user.save()
            client = Client.objects.create(user=user, first_name=self.cleaned_data['first_name'],last_name=self.cleaned_data['last_name'],
                                       birth_day=self.cleaned_data['birth_day'],
                                       email=user.email, phone=self.cleaned_data['phone'],address=self.cleaned_data['address'],
                                       profession=self.cleaned_data['profession'],company=self.cleaned_data['company'])
        return user


class ProjectForm(forms.Form):
    title = forms.CharField(max_length=100)
    catagories = forms.ChoiceField(choices=ProjectModel.P_CATAGORY)
    description = forms.CharField(widget=forms.Textarea)
    budget = forms.DecimalField(max_digits=10, decimal_places=2)
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})) 
    

class ApplicationForm(forms.Form):
    message = forms.CharField(max_length=100)
    


class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6)

# class Message(forms.Form):
#     message_test = forms.Textarea(max_)