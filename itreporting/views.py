from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Issue
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from .models import Course
from .forms import ContactForm, RegistrationForm
from django.core.mail import send_mail
from django.contrib import messages
from .models import Module
from itreporting.models import Registration



def home(request):
    return render(request, 'itreporting/home.html', {'title': 'Welcome'})

def about(request):
    return render(request, 'itreporting/about.html',)

def report(request):
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

def courses(request):
    courses = Course.objects.all()  
    return render(request, 'itreporting/courses.html', {'courses': courses, 'title': 'Courses'})

class CourseDetailView(DetailView):
    model = Course
    template_name = 'itreporting/courses_detail.html'

class CourseListView(ListView):
    model = Course
    ordering = ['-start_date']
    template_name = 'itreporting/courses.html'
    context_object_name = 'courses'
    paginate_by = 5
    

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'description', 'start_date']
    template_name = 'itreporting/courses_form.html'

    
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ['title', 'description', 'start_date']
    

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('courses')

 

class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 5 

class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields = ['type', 'room', 'urgent', 'details']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields = ['type', 'room', 'details']

    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    success_url = '/report'

    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author
    
class ModuleListView(ListView):
    model = Module
    template_name = 'itreporting/modules.html'
    context_object_name = 'modules'
    paginate_by = 5 
    
   # def get_queryset(self):
 
        #user_profile = self.request.user.profile  # Get the logged-in user's profile
        #if user_profile.course:
            # Filter modules by the user's enrolled course
           # return Module.objects.filter(courses_allowed=user_profile.course)
        #return Module.objects.none()

class ModuleDetailView(DetailView):
    model = Module
    template_name = 'itreporting/modules_detail.html'


    

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            description = f"Message from {name} via Contact Form"
            body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
            receiver = 'owencode54@gmail.com' #Email which recieves the message

            try:
                send_mail(subject, body, email, [receiver])
                messages.success(request, "Thanks for contacting Leicester University.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}. Please fill out the form again")

            return render(request, 'itreporting/contact.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'itreporting/contact.html', {'form': form})

@login_required
def register_module(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            module = form.cleaned_data['module']
            
            if Registration.objects.filter(student=request.user, module=module).exists():
                messages.error(request, f"You are already registered for this module !: {module.name}.")
            else:
                registration = form.save(commit=False)
                registration.student = request.user
                registration.save()
                messages.success(request, f"Thank you , registration succesful!: {module.name}.")
    else:
        form = RegistrationForm()

    return render(request, 'itreporting/register_module.html', {'form': form})


@login_required
def my_modules(request):
    registrations = Registration.objects.filter(student=request.user)
    return render(request, 'itreporting/my_modules.html', {'registrations': registrations})