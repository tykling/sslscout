from django.contrib import admin
from sslscout.models import Profile, SiteGroup, Site, CheckEngine, SiteCheck, RequestLog, SiteCheckLog, SiteCheckResult

admin.site.register(Profile)
admin.site.register(SiteGroup)
admin.site.register(Site)
admin.site.register(CheckEngine)
admin.site.register(SiteCheck)
admin.site.register(RequestLog)
admin.site.register(SiteCheckLog)
admin.site.register(SiteCheckResult)