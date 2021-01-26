from django.shortcuts import Http404, HttpResponseRedirect, get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import modelformset_factory

from .forms import AddressForm, JobForm, UserPictureForm
from .models import Job, Address, UserPicture
from django.urls import reverse

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

def edit_profile(request):
    # address formset
    addresses = Address.objects.filter(user=request.user)
    AddressFormSet = modelformset_factory(Address, AddressForm, extra=1, max_num=5)
    formset_a = AddressFormSet(queryset=addresses)

    # job address formset
    jobs = Job.objects.filter(user=request.user)
    JobFormSet = modelformset_factory(Job, JobForm, extra=1, max_num=5)
    formset_j = JobFormSet(queryset=jobs)

    user_picture = get_object_or_404(UserPicture, user=request.user)
    user_picture = UserPicture.objects.get(user=request.user)
    user_picture_form = UserPictureForm(request.POST or None, request.FILES or None, prefix="user_picture", instance=user_picture)
    if  user_picture_form.is_valid():
        form3 = user_picture_form.save(commit=False)
        form3.save()
    context = {
        'user_picture_form': user_picture_form,
        'formset_a': formset_a,
        'formset_j': formset_j,
    }
    return render(request, "profiles/edit_profile.html", context)

def edit_location(request):
    if request.method == "POST": 
        addresses = Address.objects.filter(user=request.user)
        AddressFormSet = modelformset_factory(Address, AddressForm, extra=1, max_num=5)
        formset_a = AddressFormSet(request.POST or None, queryset=addresses)
        if formset_a.is_valid():
            for form in formset_a:
                new_form = form.save(commit=False)
                new_form.user= request.user
                new_form.save()
            messages.success(request, "location detail updated successfully.")
            return redirect("profiles:edit")
        else:
            messages.error(request, "location detail could not updated please try again.")
            return HttpResponseRedirect(reverse("profiles:edit"))
        context = {
            'formset_a': formset_a, 
        }
        return render(request, "profiles/edit_address.html", context)
    else:
        raise Http404

def edit_job(request):
    if request.method == "POST": 
        jobs = Job.objects.filter(user=request.user)
        JobFormSet = modelformset_factory(Job, JobForm, extra=1, max_num=5)
        formset_j = JobFormSet(request.POST or None, queryset=jobs)
        if formset_j.is_valid():
            for form in formset_j:
                new_form = form.save(commit=False)
                new_form.save()
            messages.success(request, "profile jobs edited successfully.")
            return redirect("profiles:edit")
        else:
            messages.error(request, "profile jobs couldn't update please try again.")
            return HttpResponseRedirect(reverse("profiles:edit"))
        context = {
            'formset_j': formset_j,
        }
        return render(request, "profiles/edit_job.html", context)
    else:
        raise Http404