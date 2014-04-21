from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms

import datetime, hashlib, pytz, requests, uuid
from time import gmtime, strftime
from decimal import Decimal

from sslscout.models import Profile, SiteGroup, Site, CheckEngine, CheckQueue, CheckResult
from sslscout.forms import ProfileForm, SiteGroupForm


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
    form = ProfileForm(request.POST or None, instance=profile)

    ### check if the form has been POSTed and is valid
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/profile/')
    
    ### return response
    return render(request,'edit_profile.html', {
        'profile': profile,
        'form': form
    })


### add/edit sitegroup function
@login_required
def sitegroup(request,sitegroupid=None):
    if sitegroupid:
        sitegroup = get_object_or_404(SiteGroup, id=sitegroupid, user=request.user)
        form = SiteGroupForm(request.POST or None, instance=sitegroup)
        template = 'edit_sitegroup.html'
    else:
        form = SiteGroupForm(request.POST or None)
        template = 'add_sitegroup.html'

    if form.is_valid():
        sg = form.save(commit=False)
        sg.user=request.user
        sg.save()
        return HttpResponseRedirect('/sitegroups/')

    return render(request, template, {
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

