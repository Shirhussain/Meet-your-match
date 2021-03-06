import datetime
from django.urls import reverse
from django.shortcuts import Http404, HttpResponseRedirect, get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import modelformset_factory

from .forms import AddressForm, JobForm, UserPictureForm
from .models import Job, Address, UserPicture
from matches.models import JobMatch, Match, MatchList
from questions.matching import match_percentage

def home(request):
    context = {

    }
    return render(request, "home.html", context)

def subscribe(request):
    if request.user.is_authenticated:
        # subscription choice 
        # assign that choices after successful payment
        # collect create card here too
        return render(request, "profiles/subscribe.html", {})
    else:
        return render(request, "home.html")

def all(request):
    if request.user.is_authenticated:
        users = User.objects.filter(is_active=True)
        try:
            # matches = Match.objects.user_mataches(request.user)
            matches = MatchList.objects.filter(user=request.user)
        except:
            # if the user is not logged in so code should pass
            matches = []
            pass 
            
        context = {
            'users': users,
            'matches': matches,
        }
        return render(request, "profiles/all.html", context)
    else:
        return render(request, "home.html")
        
def single_user(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404

    try:
        viewed = MatchList.objects.get(user=request.user, match=user)
        viewed.read = True
        if viewed.read_at is None:
            viewed.read_at = datetime.datetime.now()
        viewed.save()
    except:
        pass
    
    set_match, created = Match.objects.get_or_create(from_user=request.user, to_user=user)
    set_match.percent = round(match_percentage(request.user, user), 2)
    # for line below the order is not importnat because of the way i wrote the algorithm
    set_match.good_match = Match.objects.good_match(request.user, user)
    set_match.save()
    # the code bellow the order is doesn't matter because it's two sided now but for points it's matter 
    # because that one is one sided 
    # match = match_percentage(request.user, single_user)
    # because the above code retune a big number i need to rounded so here we go, it give me just for digit after '.'
    
    if set_match.good_match:
        user_jobs = Job.objects.filter(user=user)
        if len(user_jobs)>0:
            for job in user_jobs:
                # i use get_or_create because i don't wanna create every time a new instance
                job_match, created = JobMatch.objects.get_or_create(user=request.user, job=job)
                print("This is Job matches: ", job_match)
                job_match.save()

    match = set_match.percent*100
    context = {
        'user': user,
        'match': match
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