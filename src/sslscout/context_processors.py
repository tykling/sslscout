from sslscout.models import CheckQueue, Site, SiteGroup
from django.conf import settings

def queuelength(request):
    if user.is_authenticated:
        queuelength = CheckQueue.objects.filter(finished=False).count()
        userqueuelength = CheckQueue.objects.filter(site__sitegroup__user=request.user).count()
        sitegroupcount = SiteGroup.objects.filter(user=request.user).count()
        sitecount = Site.objects.filter(sitegroup__user=request.user).count()
    else:
        queuelength = 0
        userqueuelength = 0
        sitegroupcount = 0
        sitecount = 0
    
    return {
        'queuelength': queuelength,
        'userqueuelength': userqueuelength,
        'sitegroupcount': sitegroupcount,
        'sitecount': sitecount,        
    }

def site(request):
    return {'SITE_URL': settings.SITE_URL}