from django.contrib import admin
from .models import Issue
admin.site.register(Issue)
from .models import Module, Course, Registration

# Register your models here.

admin.site.register(Module)

admin.site.register(Course)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'registration_date')
    search_fields = ('student__username', 'module__name')
    list_filter = ('registration_date',)