from django.shortcuts import render, Http404
from django.contrib.auth.models import User

def home(request):
    context = {

    }
    return render(request, "home.html", context)

def all(request):
    users = User.objects.filter(is_active=True)
    context = {
        'users': users,
    }
    return render(request, "profiles/all.html", context)

def single_user(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    context = {
        'user': user
    }
    return render(request, "profiles/profile.html", context)