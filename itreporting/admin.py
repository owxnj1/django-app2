from django.contrib import admin
from .models import Issue
admin.site.register(Issue)
from .models import Module, Course

# Register your models here.

admin.site.register(Module)

admin.site.register(Course)
