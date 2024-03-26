# admin.py

from django.contrib import admin
from .models import CV, JobOffer

admin.site.register(CV)
admin.site.register(JobOffer)
