from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView


app_name = 'itreporting'


urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name = 'contact'),
    path('report/', PostListView.as_view(), name = 'report'),
    path('courses/', views.courses, name='courses'),
    path('issues/<int:pk>', PostDetailView.as_view(), name = 'issue-detail'),
    path('issue/new', PostCreateView.as_view(), name = 'issue-create'),
    path('issues/<int:pk>/update/', PostUpdateView.as_view(), name = 'issue-update'),
    path('issue/<int:pk>/delete/', PostDeleteView.as_view(), name = 'issue-delete'),
    path('courses/', views.CourseListView.as_view(), name='courses'),  # List view for courses
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),  # Create view
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),  # Detail view
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),  # Update view
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
               ]

