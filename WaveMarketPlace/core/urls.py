from django.urls import path
from core.views import home,FreelencerView,user_login,ClientRegistrationView,NewProjectPostView,ProjectDetailsListView,ApplyProjectApplication
from core.views import verification_account,showAllClient,showAllFrelancer,sent_message,ProfileView, FreelancerProfileEditView

urlpatterns = [
    path('',home,name='homepage'),
    # path('login/',user_login,name='login'),
    path('free/', FreelencerView.as_view(), name='freelancer_signup'),
    path('login/',user_login,name='login'),
    path('cl/',ClientRegistrationView.as_view(),name='client_signup'),
    path('post/', NewProjectPostView,name='project_post'),
    path('list/', ProjectDetailsListView, name='project_list'),
    path('list/<int:id>',ApplyProjectApplication,name='list'),
    path('verify/', verification_account, name='verification'),
    path('client/', showAllClient, name='showClient'),
    path('freelancer/', showAllFrelancer, name='showFreelancer'),
    path('msg/', sent_message, name='sentmsg'),
    path('profile/', ProfileView, name='profile'),
    # path('edit/',FreelancerProfileEditView,name='edit'),
    # path('edit-profile/', FreelancerProfileEditView.as_view(), name='edit-profile'),
    path('edit-profile/<int:pk>/', FreelancerProfileEditView.as_view(), name='edit-profile'),

]