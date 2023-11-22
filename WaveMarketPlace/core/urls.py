from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import home,FreelencerView,user_login,ClientRegistrationView,NewProjectPostView,ProjectDetailsListView,ApplyProjectApplication
from core.views import verification_account,showAllClient,showAllFrelancer,sent_message,ProfileView, FreelancerProfileEditView,dashboard,BookmarkJob,BookmarkJobView,deleteBookmark
from core.views import JobDetailsView,freelancerGridView,ClientJobView,ClientReceiveApplicationView,FreelancerProfileView,freelancer_profile,clientdashboard,ApproveProjectFreelancer
from core.views import RejectProjectFreelancer,search_item,homepage_freelancer,FreelancerAcceptProjectList,Submission_project_view,Submission_Project_File,PaymentCheckout,success_view
from core.views import ClientProfileView,LogoutView,sign_up_user

urlpatterns = [
    path('',home,name='home'),
    path('f',homepage_freelancer,name='home1'),
    path('dashboard/',dashboard,name='dashboard'),
    # path('login/',user_login,name='login'),
    path('sign-up/', FreelencerView.as_view(), name='freelancer_signup'),
    path('sign-in/',user_login,name='login'),
    # Google Auth Login
    path('client-sign-up/',ClientRegistrationView.as_view(),name='client_signup'),
    path('client-job-post/', NewProjectPostView,name='job_post'),
    path('job-list/', ProjectDetailsListView, name='project_list'),
    path('job-list/<int:id>',ApplyProjectApplication,name='job-list'),
    path('sign-up-verify/', verification_account, name='verification'),
    path('client/', showAllClient, name='showClient'),
    path('freelancer/', showAllFrelancer, name='showFreelancer'),
    path('msg/', sent_message, name='sentmsg'),
    path('profile/', ProfileView, name='profile'),
    # Search item 
    path('search/',search_item,name='search_title'),
    # path('edit/',FreelancerProfileEditView,name='edit'),
    # path('edit-profile/', FreelancerProfileEditView.as_view(), name='edit-profile'),
    path('edit-profile/<int:pk>/', FreelancerProfileEditView.as_view(), name='edit-profile'),
    # Add Bookmark job 
    path('bookmark-add/<int:id>/',BookmarkJob,name='bookmark'),
    #Bookmark View the Template
    path('bookmark/',BookmarkJobView,name='bookmarkview'),
    #Bookmark Delete from the Template
    path('bookmark-delete/<int:project_id>/',deleteBookmark,name='deleteBookmark'),
    
    # job Details 
    path('job-details/<int:project_id>/',JobDetailsView,name='jobdetails'),
    
    #freelancer Homepage :
    path('home-freelancer/',homepage_freelancer,name='homepage_freelacer'),
    
    #freelancer Grid 
    path('candidate-grid/',freelancerGridView,name='cadidate-grid'),
    #Client Job View
    path('client-job-list/',ClientJobView,name='clientjobview'),
    #Job to Applicant/Candidate
    path('candidate-list/<int:project_id>',ClientReceiveApplicationView,name='candidatelist'),
    
    #Add Profile of Freelancer
    path('freelancer-profile-edit/',FreelancerProfileView,name='FreelancerProfileEdit'),
    path('freelancer-profile/',freelancer_profile,name='FreelancerProfile'),
    
    #client Dashboard
    path('client-dashboard/',clientdashboard,name='clientdashboard'),
    #freelancer for candidate accept or reject the application
    path('approve-apply/<int:freelancer_id>/<int:project_id>',ApproveProjectFreelancer,name='approve'),
    path('reject-apply/<int:freelancer_id>/<int:project_id>',RejectProjectFreelancer,name='reject'),   
    
    #Accept 
    path('client-dashboard-list-bd/',FreelancerAcceptProjectList,name='list_a'),
    path('submission-project-form/<int:project_id>',Submission_project_view,name='submission-form'),
    path('submission-file',Submission_Project_File,name='submission-file'),
    
    #Payment 
    path('paymet/<int:project_id>',PaymentCheckout,name='paybills'),
    path('payment/success',success_view,name='payment_success'),
    
    #Profile of CLient
    path('client/profile/edit',ClientProfileView, name='client_profile_edit'),
    
    #logout
    path('logout/', LogoutView.as_view(), name='logout'),
    
    #user type
    path('user-type/', sign_up_user, name='user_type')
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)