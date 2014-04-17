from sslscout.models import CheckQueue, Site, SiteGroup
from django.conf import settings

def queuelength(request):
    queuelength = CheckQueue.objects.filter(finished=False).count()
    userqueuelength = CheckQueue.objects.filter(site__sitegroup__user=request.user).count()
    sitegroupcount = SiteGroup.objects.filter(user=request.user).count()
    sitecount = Site.objects.filter(sitegroup__user=request.user).count()

    return {
        'queuelength': queuelength,
        'userqueuelength': userqueuelength,
        'sitegroupcount': sitegroupcount,
        'sitecount': sitecount,        
    }

def site(request):
    return {'SITE_URL': settings.SITE_URL}