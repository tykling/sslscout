from sslscout.models import CheckQueue, Site, SiteGroup
from django.conf import settings

def getstats(request):
    if request.user.is_authenticated():
        queuelength = SiteCheck.objects.exclude(finish_time__isnull=True).count()
        sitegroupcount = SiteGroup.objects.filter(user=request.user).count()
        sitecount = Site.objects.filter(sitegroup__user=request.user).count()
    else:
        queuelength = 0
        sitegroupcount = 0
        sitecount = 0

    return {
        'queuelength': queuelength,
        'sitegroupcount': sitegroupcount,
        'sitecount': sitecount,
    }

### return SITE_URL from settings.py
def site(request):
    return {'SITE_URL': settings.SITE_URL}
