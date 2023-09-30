from django.contrib import admin
from .models import User,Freelencer,Client,ApplicationModel,ProjectModel

# Register your models here.

admin.site.register(User)
admin.site.register(Freelencer)
admin.site.register(Client)
admin.site.register(ProjectModel)
admin.site.register(ApplicationModel)

