
from django.urls import path
from .views import process_cv, job_offers, apply_job, home, profile_view, job_info

urlpatterns = [
    path('', home, name='home'),
    path('process-cv/', process_cv, name='process_cv'),
    path('job-offers/', job_offers, name='job_offers'),
    path('apply-job/<int:offer_id>/', apply_job, name='apply_job'),
    path('accounts/profile/', profile_view, name='profile'),
    path('job-info/<int:offer_id>/', job_info, name='job_info'),
         
   
    
   
]
