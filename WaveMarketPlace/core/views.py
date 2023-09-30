from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import FreelancerSignUpForm, ClientSignupForm, LoginForm, ProjectForm, ApplicationForm ,VerificationForm
from .models import Freelencer, Client, User, ProjectModel, ApplicationModel ,Message,VerificationModel
from django.views.generic import CreateView
from django.contrib.auth import login
import random 
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from core.email import sent_email_verification


# Create your views here.


def home(request):
    return HttpResponse("Hello World!")


# user login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"])
        if user is not None:
            if user.is_freelencer:
                login(request, user)
                return HttpResponse("Authenticated User Successfully Login! You are Freelancer")
            elif user.is_client:
                login(request, user)
                list = Client.objects.all()
                print(list)
                return HttpResponse("Authenticated User Successfully Login! You are Client")
            else:
                return HttpResponse("Diable")
        else:
            return HttpResponse("Invalid Login")

    else:
        form = LoginForm()
    return render(request, 'login.html', {'data': form})


# Freelancer Account (Registration)
class FreelencerView(CreateView):
    model = User
    form_class = FreelancerSignUpForm
    template_name = './signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user-type'] = 'freelencer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        name = form.cleaned_data['full_name']
        print(f'Registration Name : {name} Email :{email}')
        user = form.save()
        #for sent verification code
        verification_code = sent_email_verification(email,name)
        
        #Verification Model to save code 
        verification_instance = VerificationModel(code=verification_code,user_id=user.id)
        verification_instance.save()
        
        login(self.request, user)
        return redirect('verification')


# Client Account (Registration)
class ClientRegistrationView(CreateView):
    model = User
    form_class = ClientSignupForm
    template_name = './signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user-type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        name = form.cleaned_data['username']

        user = form.save()
        #for sent verification code
        verification_code = sent_email_verification(email,name)
        
        #Verification Model to save code 
        verification_instance = VerificationModel(code=verification_code,user_id=user.id)
        verification_instance.save()
        
        login(self.request, user)
        return redirect('verification')

# Verification Page
@login_required
def verification_account(request):
    if request.method == 'POST':
        forms = VerificationForm(request.POST)
        # print(forms)
        if forms.is_valid():
            code = forms.cleaned_data['code']
            code_instance = VerificationModel.objects.get(user_id=request.user.id)
          
            if code_instance.is_verify == False:
                if code_instance.code == int(code):
                    code_instance.is_verify = True
                    code_instance.save()
                    return HttpResponse('Verification Successfull!')
                elif code_instance.code != int(code):
                    return HttpResponse("Code Error!")
            else:
                return HttpResponse("Already Verified!")
    return render(request, 'verification.html')


# New Project Post
@login_required
def NewProjectPostView(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            # Extract form data
            title = form.cleaned_data['title']
            catagories = form.cleaned_data['catagories']
            description = form.cleaned_data['description']
            budget = form.cleaned_data['budget']
            deadline = form.cleaned_data['deadline']

            client_instance = Client.objects.get(user=request.user)
            
            # Create a new ProjectModel instance
            project = ProjectModel(
                client_id=client_instance,
                title=title,
                catagories=catagories,
                description=description,
                budget=budget,
                deadline=deadline
            )
            project.save()

            return HttpResponse('Successfully Posted')
    else:
        form = ProjectForm()
    return render(request, 'project.html', {'projectform': form})


# show project Details
def ProjectDetailsListView(request):
    projectdata = ProjectModel.objects.all()
    return render(request, 'projectshow.html', {'details': projectdata})


# Apply for a Job
@login_required
def ApplyProjectApplication(request, id):
    project = ProjectModel.objects.get(id=id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data['message']
            freelancer = Freelencer.objects.get(user=request.user)
            application = ApplicationModel(
                freelencer=freelancer,
                project=project,
                message=message,
            )
            application.save()
            return HttpResponse("Application Accepted!")
    else:
        form = ApplicationForm
    return render(request, 'application.html', {'data': form})



def showAllClient(request):
    user_clients = User.objects.filter(is_client=True)
    print(user_clients)
    return render(request, 'index.html', {'data': user_clients})

def showAllFrelancer(request):
    user_freelancer = Freelencer.objects.all()
    print(user_freelancer)
    return render(request,'index.html',{'data':user_freelancer})

def sent_message(request):
    print("View called with method:", request.method)
    if request.method == 'POST':
        sender = request.user
        receiver_id = request.POST['id'] # To solve the username to found details 
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(sender=sender, receiver=receiver, message=message)
        # return JsonResponse({'message':'Message Sent Successfully.'}) 
        return render(request,'message.html',{'data':message})
    else:
        return render(request,'message.html') 
    
    
@login_required
def ProfileView(request):
    if request.user.is_client == True :
        details_data = Client.objects.get(user_id=request.user.id)
        print(details_data.email)
        # print("Client")
        return render(request,'profile.html',{'data':details_data})
    elif request.user.is_freelencer == True: 
        details_data = Freelencer.objects.get(user_id = request.user.id)
        print(details_data.email) 
        print("Freelancer")   
        return render(request,'profile.html',{'data':details_data})
    return render(request,'profile.html')
        


# @login_required
# def ProfileEdit(request,id):
#     details = Freelencer.objects.get(user_id = id)
#     print(details)
#     if request.method == 'POST':
#         form = FreelancerSignUpForm(request.POST,instance=details)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')    
#     else:
#         form = FreelancerSignUpForm()
        
#     return render(request,'edit_profile.html',{'data':form})
        
# @login_required
# def ProfileEdit(request):
#     details = Freelencer.objects.get(user=request.user)
#     if request.method == 'POST':
#         form = FreelancerSignUpForm(request.POST, instance=details)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = FreelancerSignUpForm(instance=details)
    
#     return render(request, 'edit_profile.html', {'form': form})


# class FreelancerProfileEditView(FreelencerView):
#     template_name = './edit_profile.html'

#     def get_object(self):
#         return Freelencer.objects.get(user=self.request.user)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['freelancer'] = self.get_object()
#         return context

#     def form_valid(self, form):
#         freelancer = self.get_object()
#         freelancer.full_name = form.cleaned_data['full_name']
#         freelancer.birth_day = form.cleaned_data['birth_day']
#         freelancer.email = form.cleaned_data['email']
#         freelancer.phone = form.cleaned_data['phone']
#         freelancer.address = form.cleaned_data['address']
#         freelancer.skill = form.cleaned_data['skill']
#         freelancer.save()

#         return redirect('profile') 

# class FreelancerProfileEditView(FreelencerView):
#     template_name = './edit_profile.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['Freelencer'] = self.get_object()
#         return context

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         instance = self.get_object()
#         form.fields['full_name'].initial = instance.full_name
#         form.fields['birth_day'].initial = instance.birth_day
#         form.fields['email'].initial = instance.email
#         form.fields['phone'].initial = instance.phone
#         form.fields['address'].initial = instance.address
#         form.fields['skill'].initial = instance.skill
#         return form


class FreelancerProfileEditView(FreelencerView):
    model = User
    template_name = './edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Freelancer'] = self.get_object()
        return context


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        instance = self.get_object()
        
        try:
            model = User
            # print(User.get_username)
            print(model.username)
            # print(user.username)
            profile = Freelencer.objects.get(user=instance) 
            # profile = Freelencer.objects.get(user=instance)
            # user_details = User.objects.get(profile.user_id)
            # form.fields['username'].initial = user_details.username
            form.fields['full_name'].initial = profile.full_name
            form.fields['birth_day'].initial = profile.birth_day
            form.fields['email'].initial = profile.email
            form.fields['phone'].initial = profile.phone
            form.fields['address'].initial = profile.address
            form.fields['skill'].initial = profile.skill
        except Freelencer.DoesNotExist:
            pass  # Handle the case where the user doesn't have a profile
        
        return form