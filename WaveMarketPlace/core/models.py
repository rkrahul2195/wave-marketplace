from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_freelancer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    
    # user_groups = models.ManyToManyField('auth.Group', related_name='user_custom_users', blank=True)
    user_groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True)


class Freelencer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_day = models.DateField()
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username

# class FreelancerProfileModel(models.Model):
#     freelancer = models.ForeignKey(Freelencer,on_delete=models.CASCADE)
#     about = models.TextField(blank=True,null=True)
#     skill = models.CharField(max_length=200)
#     interest = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='freelancer_profiles/') 
    
class Client(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_day = models.DateField()
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
  
    def __str__(self):
        return self.user.username

class ClientProfile(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    about = models.TextField(blank=True,null=True)
    company = models.CharField(max_length=20)
    country = models.CharField(max_length=30)
    language = models.CharField(max_length=40)
    image = models.ImageField(upload_to='client/')
    


class VerificationModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.IntegerField()
    timestamp = models.TimeField(auto_now_add=True)
    is_verify = models.BooleanField(default=False)
    
class ProjectModel(models.Model):
    P_CATAGORY = [
        ("Website Design", "Website Design"),
        ("Mobile App Developmet", "Mobile App Developmet"),
        ("Graphics Design", "Graphics Design"),
        ("AI Services", "AI Services"),
        ("Content Writting", "Content Writting"),
        ("Digital Marketing", "Digital Marketing"),
    ]
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='project/')
    catagories = models.CharField(max_length=30,choices=P_CATAGORY)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10,decimal_places=2)
    deadline = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def search_item(self,title):
        return ProjectModel.objects.filter(title__icontains=title)


    

class ApplicationModel(models.Model):
    freelencer = models.ForeignKey(Freelencer,on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectModel,on_delete=models.CASCADE)
    message = models.TextField()
    
class ApproveProject(models.Model):
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    project=models.ForeignKey(ProjectModel,on_delete=models.CASCADE)
    freelancer=models.ForeignKey(Freelencer,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)
    
class BookmarkModel(models.Model):
    freelancer = models.ForeignKey(Freelencer,on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectModel,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_messages')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver_messages')
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class FreelancerProfile(models.Model):
    freelancer = models.ForeignKey(Freelencer,on_delete=models.CASCADE)
    about = models.TextField(blank=True,null=True)
    skill = models.CharField(max_length=200)
    interest = models.CharField(max_length=100,default='')
    image = models.ImageField(upload_to='freelancer/') 
    
    
class SubmissionProjectFile(models.Model):
    project_id = models.ForeignKey(ProjectModel,on_delete=models.CASCADE)
    freelancer_id = models.ForeignKey(Freelencer,on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200)
    details = models.TextField()
    file = models.FileField(upload_to='ProjectFile/')
    timestamp = models.DateTimeField(auto_now_add=True)


class PaymentModel(models.Model):
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    client  = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    tnx_id = models.TextField(max_length=200)
    checkout = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
