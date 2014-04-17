from django.conf import settings

def queuelength(request):
    queueitems = CheckQueue.objects.filter(finished=False)
    userqueue = CheckQueue.objects.filter(user=request.user)
    return {
        'queuelength': queueitems.len(),
        'userqueuelength': userqueue.len()
    }

def site(request):
    return {'SITE_URL': settings.SITE_URL}