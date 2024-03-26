from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='cv_files/')
    text_content = models.TextField()
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class JobOffer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_experience = models.IntegerField()
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def applicants_count(self):
        return self.applications.count()

class Application(models.Model):
    offer = models.ForeignKey(JobOffer, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cv = models.ForeignKey('CVmanag.CV', on_delete=models.CASCADE)

    def __str__(self):
        return f'Application for {self.offer.title} by {self.user.username}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
class Job(models.Model):
    title = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    image = models.ImageField(upload_to='job_images/')
