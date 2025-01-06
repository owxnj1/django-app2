from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='media/profile_pics/default.jpg',upload_to='profile_pics')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
        
    
   # course = models.ForeignKey('itreporting.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def enroll_in_course(self, course):
        self.course = course
        self.save()
