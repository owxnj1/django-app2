from django.shortcuts import render
from django.http import HttpResponse
from .models import Issue
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from .models import Course

def home(request):
    return render(request, 'itreporting/home.html', {'title': 'Welcome'})

def about(request):
    return render(request, 'itreporting/about.html',)

def contact(request):
    return render(request, 'itreporting/contact.html',)

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
    

