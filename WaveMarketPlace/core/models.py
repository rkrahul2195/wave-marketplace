from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_freelencer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    
    # user_groups = models.ManyToManyField('auth.Group', related_name='user_custom_users', blank=True)
    user_groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True)


class Freelencer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    
    full_name = models.CharField(max_length=30)
    birth_day = models.DateField()
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    skill = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username



class Client(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_day = models.DateField()
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    company = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username
    

class VerificationModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.IntegerField()
    sent_time = models.TimeField(auto_now_add=True)
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
    catagories = models.CharField(max_length=30,choices=P_CATAGORY)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10,decimal_places=2)
    deadline = models.DateField()
    
    
class ApplicationModel(models.Model):
    freelencer = models.ForeignKey(Freelencer,on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectModel,on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    

class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_messages')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver_messages')
    message_text = models.TextField(max_length=200)
    sent_time = models.DateTimeField(auto_now_add=True)