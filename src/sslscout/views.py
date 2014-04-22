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
def profile_show(request):
    ### get user profile
    profile = Profile.objects.get(user=request.user)
    return render(request,'profile_details.html', {
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
    return render(request,'profile_edit.html', {
        'profile': profile,
        'form': form
    })


### add/edit sitegroup function
@login_required
def sitegroup_add_edit(request,sitegroupid=None):
    if sitegroupid:
        sitegroup = get_object_or_404(SiteGroup, id=sitegroupid, user=request.user)
        form = SiteGroupForm(request.POST or None, instance=sitegroup)
        template = 'sitegroup_edit.html'
    else:
        form = SiteGroupForm(request.POST or None)
        template = 'sitegroup_add.html'

    if form.is_valid():
        sg = form.save(commit=False)
        sg.user=request.user
        sg.save()
        return HttpResponseRedirect('/sitegroups/')

    return render(request, template, {
        'form': form
    })


### delete sitegroup
@login_required
def sitegroup_delete(request, sitegroupid):
    ### if this sitegroup doesn't exist or is not owned by this user, return 404
    sg = get_object_or_404(SiteGroup, id=sitegroupid, user=request.user)

    ### check that this sitegroup has 0 sites before deleting
    sitecount = Site.objects.filter(sitegroup=sg).count()
    if sitecount > 0:
        return render(request, 'sitegroup_delete_fail.html', {
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

    return render(request, 'sitegroup_delete_confirm.html', {
        'sg': sg,
        'form': form
    })


### list sitegroups
@login_required
def sitegroup_list(request):
    ### get a list of this users sitegroups
    sitegroups = SiteGroup.objects.filter(user=request.user)

    return render(request, 'sitegroup_list.html', {
        'sitegroups': sitegroups,
    })


### show sitegroup details
@login_required
def sitegroup_details(request,sitegroupid):
    ### if this sitegroup doesn't exist or is not owned by this user, return 404
    sg = get_object_or_404(SiteGroup, id=sitegroupid, user=request.user)
    
    return render(request, 'sitegroup_details.html', {
        'sg': sg,
    })


### list sites
@login_required
def site_list(request):
    ### get a list of this users sites
    sites = Site.objects.filter(sitegroup__user=request.user)

    return render(request, 'site_list.html', {
        'sites': sites,
    })


### add / edit site
@login_required
def site_add_edit(request,siteid=None,sitegroupid=None):
    if siteid:
        site = get_object_or_404(Site, id=siteid, user=request.user)
        form = SiteForm(request.POST or None, instance=site)
        template = 'site_edit.html'
    else:
        form = SiteForm(request.POST or None, initial={'sitegroupid': sitegroupid})
        template = 'site_add.html'

    if form.is_valid():
        site = form.save()
        return HttpResponseRedirect('/sites/')

    return render(request, template, {
        'form': form
    })


### delete site
@login_required
def site_delete(request, siteid):
    ### if this site doesn't exist or is not owned by this user, return 404
    site = get_object_or_404(Site, id=siteid, user=request.user)
    
    if request.method == 'POST':
        form = DeleteSiteForm(request.POST, instance=site)
        if form.is_valid():
            site.delete()
            return HttpResponseRedirect("/sites/")
        else:
            return HttpResponseRedirect("/sites/")
    else:
        form = DeleteSiteForm(instance=site)

    return render(request, 'site_delete_confirm.html', {
        'site': site,
        'form': form
    })


### site details
@login_required
def site_details(request, siteid):
    ### if this site doesn't exist or is not owned by this user, return 404
    site = get_object_or_404(Site, id=siteid, user=request.user)

    return render(request, 'site_details.html', {
        'site': site,
    })



