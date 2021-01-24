from django.urls import path
from . import views

app_name = "profiles"
urlpatterns = [
    path('all/', views.all, name="all"),
    path('member/<str:username>/', views.single_user, name="profile"),
]

