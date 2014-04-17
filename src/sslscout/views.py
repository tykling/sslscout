from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms
from sslscout.models import Profile
from sslscout.forms import ProfileForm
import datetime, hashlib, pytz, requests, uuid
from time import gmtime, strftime
from decimal import Decimal


### renders a static page
def staticpage(request,page):
    return render(request,page)


### show profile
@login_required
def profile(request):
    ### get user profile
    profile = Profile.objects.get(user=request.user)
    return render(request,'profile.html', {
        'profile': profile,
        'user': request.user
    })


### edit profile function
@login_required
def profile_edit(request):
    ### get the profile
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():

            ### save updated profile data
            profile.first_name = form['first_name'].data
            profile.last_name = form['last_name'].data
            profile.country = form['country'].data
            profile.save()
            return HttpResponseRedirect('/profile/')
        else:
            ### form is not valid
            form = ProfileForm(request.POST)
    else:
        form = ProfileForm(instance=profile)
    
    ### get user profile
    return render(request,'edit_profile.html', {
        'profile': profile,
        'form': form
    })
