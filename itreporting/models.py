from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from django.core.validators import EmailValidator

class Issue(models.Model):
    type = models.CharField(
        max_length=100, 
        choices=[('Hardware', 'Hardware'), ('Software', 'Software')]
    )
    room = models.CharField(max_length=100)
    urgent = models.BooleanField(default=False)
    details = models.TextField()
    date_submitted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    author = models.ForeignKey(
        User, 
        related_name='issues', 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.type} Issue in {self.room}'

    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs={'pk': self.pk})

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('itreporting:course_detail', kwargs={'pk': self.pk})
    
class Module(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    credit = models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    courses_allowed = models.ManyToManyField(Course)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('modules_detail', kwargs={'pk': self.pk})

    


