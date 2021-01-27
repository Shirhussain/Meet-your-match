from django.urls import path
from . import views

app_name = "questions"
urlpatterns = [
    path('', views.all_question, name="questions"),
]
