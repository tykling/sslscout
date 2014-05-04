from django.db import models
from django.contrib.auth.models import User
from uuidfield import UUIDField


### model for user profiles
class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=200,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    site_limit = models.IntegerField(default=1)


### contains all site groups
class SiteGroup(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    interval_hours = models.PositiveIntegerField()
    alert = models.BooleanField()

    def __unicode__(self):
        if self.alert:
            return "%s (%sh,alerting)" % (self.name,self.interval_hours)
        else:
            return "%s (%sh,no alerting)" % (self.name,self.interval_hours)


### contains all site definitions    
class Site(models.Model):
    sitegroup = models.ForeignKey(SiteGroup)
    hostname = models.CharField(max_length=256)

    def __unicode__(self):
        return self.hostname


### defines the different engines available
class CheckEngine(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    checkurl = models.CharField(max_length=200)
    engineclass = models.CharField(max_length=50)
    active = models.BooleanField(default=True)


### contains the running and finished site checks and results
class SiteCheck(models.Model):
    site = models.ForeignKey(Site)
    engine = models.ForeignKey(CheckEngine)
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True)

    debug_html = models.TextField(null=True)
    overall_rating = models.CharField(max_length=2,null=True)
    certificate_score = models.IntegerField(null=True)
    protocolsupport_score = models.IntegerField(null=True)
    keyexchange_score = models.IntegerField(null=True)
    cipherstrength_score = models.IntegerField(null=True)


### import signals from signals.py (for profile autocreation on user creation)
import signals
