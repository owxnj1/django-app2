from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, ModuleListView, ModuleDetailView


app_name = 'itreporting'


urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name = 'contact'),
    path('report/', PostListView.as_view(), name = 'report'),
    path('courses/', views.courses, name='courses'),
    path('modules/', ModuleListView.as_view(), name='modules'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='modules_detail'),
    path('issues/<int:pk>', PostDetailView.as_view(), name = 'issue-detail'),
    path('issue/new', PostCreateView.as_view(), name = 'issue-create'),
    path('issues/<int:pk>/update/', PostUpdateView.as_view(), name = 'issue-update'),
    path('issue/<int:pk>/delete/', PostDeleteView.as_view(), name = 'issue-delete'),
    path('courses/', views.CourseListView.as_view(), name='courses'),  
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'), 
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),  
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),  
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
               ]

