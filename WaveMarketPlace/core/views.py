from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FreelancerSignUpForm, ClientSignupForm, LoginForm, ProjectForm, ApplicationForm, VerificationForm
from .models import Freelencer, Client, User, ProjectModel, ApplicationModel, Message, VerificationModel, BookmarkModel, FreelancerProfile,ApproveProject,ClientProfile,SubmissionProjectFile,PaymentModel
from django.views.generic import CreateView
from django.contrib.auth import login
import random
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from core.email import sent_email_verification,sent_notification
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .ssl import unique_id,SSL_Payment
from django.contrib.auth.views import LogoutView
# Homepage

def user_profile(request_user):
     if request_user.user.is_freelancer:
        user_data = Freelencer.objects.get(user=request_user.user)
        print(user_data)
        user_profile = FreelancerProfile.objects.get(freelancer_id = user_data.user_id)
        data = {
                    'first_name' : user_data.first_name,
                    'last_name' : user_data.last_name,
                    'profile' : user_profile.image
                }
        return data
     elif request_user.user.is_client:
        user_data = Client.objects.get(user=request_user.user)
        print(user_data.first_name)
        user_profile = ClientProfile.objects.get(client=user_data)
        data = {
             'first_name' : user_data.first_name,
             'last_name' : user_data.last_name,
             'profile' : user_profile.image
        }
        return data 

def homepage_freelancer(request_user):
    projectdata = ProjectModel.objects.all()[:5]
    user_data = user_profile(request_user)
    print(user_data)
    return user_data,projectdata
        
def homepage_client(request_user):
    projectdata = ProjectModel.objects.all()[:5]
    user_data = user_profile(request_user)
    print(user_data)
    return user_data,projectdata

def home(request):
    projectdata = ProjectModel.objects.all()[:5]

    if not request.user.is_authenticated:
        print('Not User')
        return render(request, 'home.html', {'data': projectdata})  # Handle anonymous user

    elif request.user.is_freelancer:
        print('Freelancer')
        user_data, projectdata = homepage_freelancer(request)

    elif request.user.is_client:
        user_data, projectdata = homepage_client(request)
        print('Client') 
        print(projectdata)
        

    return render(request, 'home.html', {'data': projectdata, 'user_data': user_data})

    
    


def google_auth_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    return redirect('/auth/login/google-oauth2/')


def search_item(request):
    print('Test 00')
    search_item = request.GET.get('title','')
    data = ProjectModel.search_item(request,search_item)
    print('Test 01')
    return render(request,'home.html',{'data':data})
    

@login_required
def dashboard(request):
    user_details = None
    project_details = None
    
    user_data = user_profile(request)
    
    if request.user.is_freelancer:
        user_details = Freelencer.objects.get(user=request.user)
        print(user_details.user_id)
        freelancer_application = ApplicationModel.objects.filter(
            freelencer_id=user_details.user_id)
        print(freelancer_application)

        project_details = []
        for application in freelancer_application:
            project = ProjectModel.objects.get(id=application.project_id)
            project_details.append(project)
            
        
  
        context =  {'details': user_details,
                     'user_data':user_data,
                    'project_details': project_details}

    return render(request, 'dashboard.html',context)


@login_required
def ClientReceiveApplicationView(request, project_id):
    application_details = None
    project_details = None
    project_id = project_id

    if request.user.is_client:
        application_details = ApplicationModel.objects.filter(
            project_id=project_id)
        user_data,projectdata = homepage_client(request)
        print(application_details)

        project_details = []
        for candidate in application_details:
            user_details = Freelencer.objects.get(
                user_id=candidate.freelencer_id)
            freelancer_profile = FreelancerProfile.objects.get(freelancer_id=candidate.freelencer_id)
            print(user_details)
            project_details.append({
                'user_details': user_details,
                'message': candidate.message,
                'profile' : freelancer_profile.image
            })

        return render(request, 'test-candidate-list.html', {'data': project_details,'project_id':project_id,'user_data':user_data})


@login_required
def ClientJobView(request):
    Client_Job_details = None
    if request.user.is_client:
        Client_Job_details = ProjectModel.objects.filter(
            client_id_id=request.user.id)
        user_data,projectdata = homepage_client(request)
        print(Client_Job_details)

    return render(request, 'test-Client-manage-jobs.html', {'data': Client_Job_details,'user_data':user_data})



def check_user_type(user):
    if user.is_client:
        return "client"
    elif user.is_freelancer:
        return "freelancer"
    else:
        return "unknown"

# login all user (Freelancer and Client)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"])
        if user is not None:
            if user.is_freelancer:
                login(request, user)
                list = Freelencer.objects.filter(user=request.user)
                print(list)
                return redirect('dashboard')
                # return HttpResponse("Authenticated User Successfully Login! You are Freelancer")
            elif user.is_client:
                login(request, user)
                list = Client.objects.filter(user=request.user)
                print(list)
                # return HttpResponse("Authenticated User Successfully Login! You are Client")
                return redirect('clientdashboard')
            else:
                return HttpResponse("Diable")
        else:
            return HttpResponse("Invalid Login")

    else:
        form = LoginForm()
    return render(request, 'sign-in.html', {'data': form})


# Freelancer Account (Registration)
class FreelencerView(CreateView):
    model = User
    form_class = FreelancerSignUpForm
    template_name = './sign-up.html'

    def get_context_data(self, **kwargs):
        kwargs['user-type'] = 'freelencer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        name = form.cleaned_data['first_name']
        print(f'Registration Name : {name} Email :{email}')
        user = form.save()
        # for sent verification code
        verification_code = sent_email_verification(email, name)

        # Verification Model to save code
        verification_instance = VerificationModel(
            code=verification_code, user_id=user.id)
        verification_instance.save()

        login(self.request, user)
        return redirect('verification')

@login_required
def FreelancerProfileView(request):
    if request.user.is_freelancer:
        profile = Freelencer.objects.get(user_id=request.user.id)
        freelancer_profile = FreelancerProfile.objects.get(freelancer=profile)
        if request.method == 'POST':
            about = request.POST.get('about')
            skill = request.POST.get('skills')
            interest = request.POST.get('interest')
            image = request.FILES.get('image')

            freelancer_profile = FreelancerProfile(
                freelancer=profile,
                about=about,
                skill=skill,
                interest=interest,
                image=image
            )
            freelancer_profile.save()
            messages.success(request, 'Freelancer profile updated successfully!')
            return HttpResponseRedirect(reverse('FreelancerProfileEdit'))   
        else:
            # Return an HttpResponse object even if the request method is not POST.
            context = {'freelancer_profile': freelancer_profile}
            return render(request, 'test-profile.html',context)
    else:
        return render(request, 'test-profile.html')


# def freelancer_profile(request):
#     freelancer_profile = None
#     freelancer_profile = FreelancerProfile.objects.get(
#         freelancer_id=request.user.id)
    
#     if not freelancer_profile:
#         return render(request, 'test-profile.html', {'freelancer_profile': freelancer_profile})
#     else:
#         return render(request, 'test-profile.html') 
def freelancer_profile(request):
  freelancer_profile = None
  try:
    freelancer_profile = FreelancerProfile.objects.get(
      freelancer_id=request.user.id)
  except FreelancerProfile.DoesNotExist:
    pass

  if freelancer_profile:
    return render(request, 'test-profile.html', {'freelancer_profile': freelancer_profile})
  else:
    # Render a different template if the FreelancerProfile object does not exist.
    return render(request, 'test-profile.html')

        
def clientdashboard(request):
   if request.user.is_client:
       project=ProjectModel.objects.filter(client_id_id=request.user.id)
       user_details = Client.objects.get(user_id = request.user.id)
       user_data,projectdata= homepage_client(request)
       return render(request,'test-client-dashboard.html',{'project_details':project,'details':user_details,'user_data':user_data})
   return render(request,'test-client-dashboard.html')


 
# @login_required
# def ClientProfileView(request):
#     if request.user.is_client:
#         profile = Client.objects.get(user_id=request.user.id)
#         # freelancer_profile = ClientProfile.objects.get(client=profile)
#         if request.method == 'POST':
#             about = request.POST.get('about')
#             company = request.POST.get('company')
#             country = request.POST.get('country')
#             language = request.POST.get('language')
#             image = request.FILES.get('image')
            
#             if ClientProfile.objects.get(client=profile).exits():
#                 messages.success(request, 'profile updated successfully!')
#                 return HttpResponse('profile updated successfully!')
            
#             else:
#                 client_profile = ClientProfile(
#                     client = profile,
#                     about = about,
#                     company = company,
#                     country  = country,
#                     language = language,
#                     image = image
#                 )
#                 client_profile.save()
#                 messages.success(request, 'Profile updated successfully!')
#                 return HttpResponse('Successfull!')
#         else:
#             # Return an HttpResponse object even if the request method is not POST.
#             # E:\Fall 2023\WEB\Semester Project\WaveMarketPlace\core\Templates\test-client-profile.html
#             context = {'freelancer_profile': freelancer_profile}
#             return render(request, 'test-client-profile.html',context)
#     else:
#         return render(request, 'test-client-profile.html')



def ClientProfileView(request):
    if request.user.is_client:
        profile = Client.objects.get(user_id=request.user.id)

        if request.method == 'POST':
            about = request.POST.get('about')
            company = request.POST.get('company')
            country = 'Bangladesh'
            language = request.POST.get('language')
            image = request.FILES.get('image')

            client_profile = ClientProfile.objects.filter(client=profile).first()

            if client_profile:
                client_profile.about = about
                client_profile.company = company
                client_profile.country = country
                client_profile.language = language
                client_profile.image = image
                client_profile.save()
                messages.success(request, 'Profile updated successfully!')
                return HttpResponse('Profile updated successfully!')
            else:
                client_profile = ClientProfile.objects.create(
                    client=profile,
                    about=about,
                    company=company,
                    country=country,
                    language=language,
                    image=image
                )
                messages.success(request, 'Profile created successfully!')
                return HttpResponse('Profile created successfully!')
        else:
            context = {'freelancer_profile': profile}
            return render(request, 'test-client-profile.html', context)
    else:
        return render(request, 'test-client-profile.html')




# Client Account (Registration)
class ClientRegistrationView(CreateView):
    model = User
    form_class = ClientSignupForm
    template_name = './sign-up.html'

    def get_context_data(self, **kwargs):
        kwargs['user-type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        name = form.cleaned_data['username']

        user = form.save()
        # for sent verification code
        verification_code = sent_email_verification(email, name)

        # Verification Model to save code
        verification_instance = VerificationModel(
            code=verification_code, user_id=user.id)
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
            code_instance = VerificationModel.objects.get(
                user_id=request.user.id)

            if code_instance.is_verify == False:
                if code_instance.code == int(code):
                    code_instance.is_verify = True
                    code_instance.save()
                    return HttpResponse('Verification Successfull!')
                elif code_instance.code != int(code):
                    return HttpResponse("Code Error!")
            else:
                return HttpResponse("Already Verified!")
    return render(request, 'sign-up-verify.html')


@login_required
def NewProjectPostView(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        print('Check line 225')
        if form.is_valid():
            # Extract form data
            print('Check line 227')
            title = form.cleaned_data['title']
            image = form.cleaned_data['image']
            catagories = form.cleaned_data['catagories']
            description = form.cleaned_data['description']
            budget = form.cleaned_data['budget']
            deadline = form.cleaned_data['deadline']

            client_instance = Client.objects.get(user=request.user)

            # Create a new ProjectModel instance
            project = ProjectModel(
                client_id=client_instance,
                title=title,
                image=image,
                catagories=catagories,
                description=description,
                budget=budget,
                deadline=deadline
            )
            print('Check line 248')
            project.save()

            return HttpResponse('Successfully Posted')
    else:
        print('Check line 253')
        form = ProjectForm()
    return render(request, 'job-post.html', {'projectform': form})


# # New Project Post
# @login_required
# def NewProjectPostView(request):
#     # user = authenticate(request)
#     if request.user.is_client:
#         title  = request.POST.get('title')
#         catagories = request.POST.get('catagories')
#         description = request.POST.get('description')
#         budget = request.POST.get('budget')
#         deadline = request.POST.get('deadline')
#         image = request.FILES.get('image')
#         client_instance = Client.objects.get(user=request.user)

#         form = ProjectForm(request.POST,request.FILES)
#         if form.is_valid():
#             project = ProjectModel(
#             client_id=client_instance,
#             title=title,
#             image=image,
#             catagories=catagories,
#             description=description,
#             budget=budget,
#             deadline=deadline
#             )
#             print(project)
#             project.save()
#             return HttpResponse('Successfully Posted')
#         else:
#             form=ProjectForm(request.POST,request.FILES)

#     return render(request, 'job-post.html')


# show project Details
def ProjectDetailsListView(request):
    projectdata = ProjectModel.objects.all()
    if request.user.is_client:
        user_data,projectdata = homepage_client(request)
    elif request.user.is_freelancer:
        user_data,projectdata = homepage_freelancer(request)
    return render(request, 'testpost.html', {'data': projectdata,'user_data':user_data})


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
    return render(request, 'job-application.html', {'data': form})


# Bookmark Added
@login_required
def BookmarkJob(request, id):
    if request.user.is_freelancer:
        freelancer = Freelencer.objects.get(user=request.user)
        project = ProjectModel.objects.get(id=id)
    #   if already bookmark the project
        if BookmarkModel.objects.filter(freelancer=freelancer, project=project).exists():
            #   Reverse the bookmark page
            return HttpResponseRedirect(reverse('dashboard'))
        bookmark = BookmarkModel(freelancer=freelancer, project=project)
        bookmark.save()
    #   Reverse the bookmark page
        return HttpResponseRedirect(reverse('dashboard'))

# Bookmark View


@login_required
def BookmarkJobView(request):
    bookmark_details = None
    if request.user.is_freelancer:
        bookmark = BookmarkModel.objects.filter(freelancer_id=request.user.id)

        bookmark_details = []
        for bookdata in bookmark:
            project = ProjectModel.objects.get(id=bookdata.project_id)
            bookmark_details.append(project)    
        user_data = user_profile(request_user=request)
    return render(request, 'test-bookmark-jobs.html', {'data': bookmark_details, 'user_data':user_data})


# Bookmark Delete
@login_required
def deleteBookmark(request, project_id):
    if request.user.is_freelancer:
        bookmark = BookmarkModel.objects.get(project_id=project_id)
        print(bookmark)
        bookmark.delete()
        return HttpResponseRedirect(reverse('bookmarkview'))


def freelancerGridView(request):
    freelancer_details = Freelencer.objects.all()
    print(freelancer_details)
    return render(request, 'test-candidate-grid.html', {'data': freelancer_details})


def JobDetailsView(request, project_id):
    project_details = ProjectModel.objects.get(id=project_id)
    return render(request, 'testjobdetails.html', {'project': project_details})


def showAllClient(request):
    user_clients = User.objects.filter(is_client=True)
    print(user_clients)
    return render(request, 'index.html', {'data': user_clients})


def showAllFrelancer(request):
    user_freelancer = Freelencer.objects.all()
    print(user_freelancer)
    return render(request, 'index.html', {'data': user_freelancer})


def sent_message(request):
    print("View called with method:", request.method)
    if request.method == 'POST':
        sender = request.user
        # To solve the username to found details
        receiver_id = request.POST['id']
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(
            sender=sender, receiver=receiver, message=message)
        # return JsonResponse({'message':'Message Sent Successfully.'})
        return render(request, 'message.html', {'data': message})
    else:
        return render(request, 'message.html')


@login_required
def ProfileView(request):
    if request.user.is_client == True:
        details_data = Client.objects.get(user_id=request.user.id)
        print(details_data.email)
        # print("Client")
        return render(request, 'profile.html', {'data': details_data})
    elif request.user.is_freelancer == True:
        details_data = Freelencer.objects.get(user_id=request.user.id)
        print(details_data.email)
        print("Freelancer")
        return render(request, 'profile.html', {'data': details_data})
    return render(request, 'profile.html')


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
    

@login_required
def ApproveProjectFreelancer(request,freelancer_id,project_id):
    if request.user.is_client:
        project = ProjectModel.objects.get(id=project_id)
        freelancer = Freelencer.objects.get(user_id=freelancer_id)
        if ApproveProject.objects.filter(
            freelancer_id=freelancer.user_id,
            project_id=project.id
        ).exists():
            # Display an error message to the user
            return HttpResponse('The freelancer has already been approved/Reject for this project.')
        else:
            approve_project = ApproveProject(
               client_id=request.user.id,
                project_id=project.id,
                freelancer_id=freelancer.user_id,
                status= True )
            approve_project.save()
            email = freelancer.email
            name = freelancer.first_name +' '+ freelancer.last_name
            project_title = project.title
            sent_notification(email,name,project_title)
            return HttpResponse('Successfully!')    
    return render(request,'test-candidate-list.html')


#Clinet Reject the Application 

@login_required
def RejectProjectFreelancer(request,freelancer_id,project_id):
    if request.user.is_client:
        project = ProjectModel.objects.get(id=project_id)
        freelancer = Freelencer.objects.get(user_id=freelancer_id)
        if ApproveProject.objects.filter(
            freelancer_id=freelancer.user_id,
            project_id=project.id
        ).exists():
            # Display an error message to the user
            return HttpResponse('The freelancer has already been approved/Reject for this project.')
        else:
            approve_project = ApproveProject(
               client_id=request.user.id,
                project_id=project.id,
                freelancer_id=freelancer.user_id,
                status= False)
            approve_project.save()
            email = freelancer.email
            name = freelancer.first_name +' '+ freelancer.last_name
            project_title = project.title
            sent_notification(email,name,project_title)
            return HttpResponse('Successfully!')    
    return render(request,'test-candidate-list.html')


@login_required
def AcceptFreelancerList(request,project_id):
    if request.user.is_client:
        accept_details = ApproveProject.objects.get(project_id=project_id)
        user_details = Freelencer.objects.get(user_id=accept_details.freelancer_id)
        project_details = ProjectModel.objects.get(id=project_id)
        
        return render(request,'test-accept-list.html',{'data':user_details,'projectdata':project_details})

  

@login_required
def FreelancerAcceptProjectList(request):
    if request.user.is_freelancer:
        accepted_projects = ApproveProject.objects.filter(freelancer_id=request.user.id, status=True)
        project_details = []
        for accepted_project in accepted_projects:
            project = ProjectModel.objects.filter(id=accepted_project.project_id).first()
            project_details.append({
                'project': project.title,
                'id': project.id,
                'budget' : project.budget,
                'dateline' : project.deadline,
                'catagories': project.catagories,
                'image':project.image
            })

        return render(request, 'test-freelancer-manage.html', {'project_details': project_details})


@login_required
def Submission_project_view(request,project_id):
    project_details = ProjectModel.objects.get(id=project_id)
    return render(request,'test-project-submit.html', {'data': project_details})



# @login_required
# def SubmissionProjectFile(request):
#     if request.user.is_freelancer:
#         if request.method == 'POST':
#              project_id = request.POST.get('id')
#              filename = request.POST.get('filename')
#              details = request.POST.get('describtion')
#              file = request.FILES.get('file')
             
#              print(project_id)
            
#              Project = ProjectModel.objects.get(id=project_id)
#              freelancer = Freelencer.objects.get(user=request.user)
#              print(details)
             
#              submission_file = SubmissionProjectFile(
#                  project_id = Project,
#                  freelancer_id = freelancer,
#                  file_name = filename,
#                  details = details,
#                  file = file,
#                 request=request
#              )
#              submission_file.save()
#              print(669)
#              return HttpResponse('Successfully Submission File!')
             
             


def Submission_Project_File(request):
    if request.method == 'POST':
        project_id = request.POST.get('id')
        filename = request.POST.get('filename')
        description = request.POST.get('describtion')
        file = request.FILES.get('file')
        
        print(file)

        if file is None:
            messages.error(request, 'Please select a file to submit.')
            return redirect('submission-file', project_id=project_id)

    
        freelancer = Freelencer.objects.get(user=request.user)
        project = ProjectModel.objects.get(id=project_id)
        existing_submission = SubmissionProjectFile.objects.filter(project_id=project, freelancer_id=freelancer).first()
        
        if existing_submission:
            messages.error(request, 'You have already submitted a file for this project.')
            print(messages.get_messages(request))  
            return redirect('dashboard')
        
        submission_file = SubmissionProjectFile(
            project_id=project,
            freelancer_id=freelancer,
            file_name=filename,
            details =description,
            file=file
        )
        submission_file.save()

        messages.success(request, 'Your submission has been successfully received.')
        return redirect('dashboard')

    else:
        return render(request, 'test-project-submit.html')



@method_decorator(csrf_exempt, name='dispatch') 
def success_view(request):
    name = request.user
    data = request.POST
    amount = (data['value_a'])  #Amount
    user_id = data['value_c'] #user_id
    title = data['value_b']  #title
    txn_id = data['value_d']
    print(data['card_issuer'])
    # print(data['cus_email'])
    print(amount)
    print(user_id)
    print(title)
    
    client_details = Client.objects.get(pk=user_id)
    project_details = ProjectModel.objects.get(title=title)
    
    payment = PaymentModel (
        client = client_details,
        project = project_details,
        amount = amount,
        tnx_id =  txn_id,
        checkout = True   
    )  
    payment.save() 
    return HttpResponse('Success')


@login_required
def PaymentCheckout(request,project_id):
    print(request.POST)
    if PaymentModel.objects.filter(project_id=project_id).exists():
        return HttpResponse("Already Payment")
    else:
        Project_details = ProjectModel.objects.get(id=project_id)
        user_details = Client.objects.get(user=request.user)
        
        txn_id = unique_id() 
        user_id = user_details.pk
        name = str(user_details.first_name + " " + user_details.last_name)
        number = str(user_details.phone)
        email = str(user_details.email)
        amount = Project_details.budget
        address = str(user_details.address)
        item = str(Project_details.title)
        
        
        return redirect(SSL_Payment(user_id=user_id,name=name,number=number,email=email,amount=amount,address=address,id=txn_id,item=item))
        # return HttpResponse(f'{txn_id}')



class LogoutView(LogoutView):
     template_name = 'sign-out.html'
     
     
def sign_up_user(request):
    return render(request,'sign-up-user.html')