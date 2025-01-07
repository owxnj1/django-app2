from django.shortcuts import render, redirect, get_object_or_404
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
import requests



def home(request):
    api_key = "b2d64ea0ad361e5db41044f07bfdc2cc"  # Replace with your actual API key
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'

    # List of cities and countries
    cities = [('Leicester', 'UK')]

    # Fetch weather data for each city
    weather_data = []
    for city in cities:
        response = requests.get(url.format(city[0], city[1], api_key))
        if response.status_code == 200:
            city_weather = response.json()
            weather = {
                'city': city_weather['name'] + ', ' + city_weather['sys']['country'],
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description']
            }
            weather_data.append(weather)
        else:
            weather_data.append({'city': city[0], 'temperature': 'N/A', 'description': 'Data not available'})
    return render(request, 'itreporting/home.html', {'title': 'Homepage', 'weather_data': weather_data})

def about(request):
    api_key = "b2d64ea0ad361e5db41044f07bfdc2cc"  # Replace with your actual API key
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'

    # List of cities and countries
    cities = [('Leicester', 'UK')]

    # Fetch weather data for each city
    weather_data = []
    for city in cities:
        response = requests.get(url.format(city[0], city[1], api_key))
        if response.status_code == 200:
            city_weather = response.json()
            weather = {
                'city': city_weather['name'] + ', ' + city_weather['sys']['country'],
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description']
            }
            weather_data.append(weather)
        else:
            weather_data.append({'city': city[0], 'temperature': 'N/A', 'description': 'Data not available'})
    return render(request, 'itreporting/about.html', {'title': 'About', 'weather_data': weather_data})

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
def register_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)

    if not module.availability:
                messages.error(request, f"Sorry, the module '{module.name}' is currently closed for registration.")
                return redirect('itreporting:my_modules')  

    if Registration.objects.filter(student=request.user, module=module).exists():
        messages.error(request, f"You have aleady registered for this module, please slect a new one!: {module.name}.")
    else:
        Registration.objects.create(student=request.user, module=module)
        messages.success(request, f"You have now registered for this module, thank you!: {module.name}.")

    return redirect('itreporting:my_modules')


@login_required
def my_modules(request):
    registrations = Registration.objects.filter(student=request.user)
    profile_image = request.user.profile.image.url if request.user.profile.image else '/media/profile_pics/default.jpg'
    return render(request, 'itreporting/my_modules.html', {'registrations': registrations,'profile_image': profile_image})


@login_required
def unregister_module(request, module_id):

    module = get_object_or_404(Module, id=module_id)

    registration = Registration.objects.filter(student=request.user, module=module).first()
    if registration:
        registration.delete()
        messages.success(request, f"You have successfully unregistered from the module: {module.name}.")
    else:
        messages.error(request, f"You are not registered for the module: {module.name}.")
    
    return redirect('itreporting:my_modules')