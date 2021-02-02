from django.urls import path
from . import views

app_name = "directmessages"
urlpatterns = [
    path('inbox/', views.inbox, name="inbox"),
    path('sent/', views.sent, name="sent"),
    path('compose/', views.compose, name="compose"),
    path('view/<int:id>/', views.direct_message_view, name="view"),
    path('view/<int:id>/reply/', views.reply, name="reply"),
]

