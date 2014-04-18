import datetime, hashlib, pytz, requests, uuid
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms
from sslscout.models import Profile, SiteGroup, Site, CheckEngine, CheckQueue, CheckResult
from sslscout.forms import ProfileForm, SiteGroupForm
from time import gmtime, strftime
from decimal import Decimal


### renders any static page
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
    
    ### return response
    return render(request,'edit_profile.html', {
        'profile': profile,
        'form': form
    })


@login_required
### add sitegroup
def add_sitegroup(request):
    if request.method == 'POST':
        form = SiteGroupForm(request.POST)
        if form.is_valid():
            ### validate interval
            if form['interval_hours'].data > 0:
                ### create new sitegroup
                sg = SiteGroup()
                
                ### add values from form
                sg.user = request.user()
                sg.interval_hours = form['interval_hours'].data
                sg.alert = form['alert'].data
                sg.save()
                
                return HttpResponseRedirect('/sitegroups/')
        else:
            ### form is not valid
            form = SiteGroupForm(request.POST)
    else:
        form = SiteGroupForm()
    
    ### return response
    return render(request,'add_sitegroup.html', {
        'form': form
    })


@login_required
### edit sitegroup
def edit_sitegroup(request,sitegroupid):
    sg = get_object_or_404(SiteGroup, id=sitegroupid)
    if request.method == 'POST':
        form = SiteGroupForm(request.POST)
        if form.is_valid():        
            ### add values from form
            sg.user = request.user()
            sg.interval_hours = form['interval_hours'].data
            sg.alert = form['alert'].data
            sg.save()
            return HttpResponseRedirect('/sitegroups/')
        else:
            ### form is not valid
            form = SiteGroupForm(request.POST)
    else:
        form = SiteGroupForm(instance=sg)
    
    ### return response
    return render(request,'edit_sitegroup.html', {
        'form': form
    })


@login_required
### delete sitegroup
def delete_sitegroup(request, sitegroupid):
    ### if this sitegroup doesn't exist or is not owned by this user, return 404
    sg = get_object_or_404(SiteGroup, id=sitegroupid, user=request.user)

    ### check that this sitegroup has 0 sites before deleting
    sitecount = Site.objects.filter(sitegroup=sg).count()
    if sitecount > 0:
        return render(request, 'delete_sitegroup_fail.html', {
            'sg': sg,
            'sitecount': sitecount
        })
    
    if request.method == 'POST':
        form = DeleteSiteGroupForm(request.POST, instance=sg)
        if form.is_valid():
            fg.delete()
            return HttpResponseRedirect("/sitegroups/")
        else:
            return HttpResponseRedirect("/sitegroups/")
    else:
        form = DeleteNewForm(instance=sg)

    return render(request, 'delete_sitegroup_confirm.html', {
        'sg': sg,
        'form': form
    })


@login_required
### list sitegroups
def list_sitegroups(request):
    ### get a list of this users sitegroups
    sitegroups = SiteGroup.objects.filter(user=request.user)

    return render(request, 'list_sitegroups.html', {
        'sitegroups': sitegroups,
    })

