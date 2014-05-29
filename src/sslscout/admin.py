from django.contrib import admin
from sslscout.models import Profile, SiteGroup, Site, CheckEngine, SiteCheck, RequestLog, SiteCheckLog

admin.site.register(Profile)
admin.site.register(SiteGroup)
admin.site.register(Site)
admin.site.register(CheckEngine)
admin.site.register(SiteCheck)
admin.site.register(ZipzapEnvironment)
admin.site.register(RequestLog)
admin.site.register(SiteCheckLog)
