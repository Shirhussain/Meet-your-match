from django.urls import path
from . import views

app_name = "profiles"
urlpatterns = [
    path('member/<str:username>/', views.single_user, name="profile"),
    path('edit/', views.edit_profile, name="edit"),
    path('edit/jobs/', views.edit_job, name="edit_jobs"),
    path('edit/locations/', views.edit_location, name="edit_locations"),
]

