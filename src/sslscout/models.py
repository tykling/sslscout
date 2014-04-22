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


### contains all site definitions    
class Site(models.Model):
    sitegroup = models.ForeignKey(SiteGroup)
    hostname = models.CharField(max_length=256)

    def __unicode__(self):
        return self.hostname


### defines the different engines available
class CheckEngine(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField()


### the check queue
class CheckQueue(models.Model):
    site = models.ForeignKey(Site)
    engine = models.ForeignKey(CheckEngine)
    finished = models.BooleanField(default=False)
    queue_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)
    debug_html = models.TextField(null=True)


### contains all check results
class CheckResult(models.Model):
    site = models.ForeignKey(Site)
    check_queue_id = models.ForeignKey(CheckQueue)
    check_finish_datetime = models.DateTimeField(auto_now_add=True)
    overall_rating = models.CharField(max_length=2,null=True)
    certificate_score = models.IntegerField(null=True)
    protocolsupport_score = models.IntegerField(null=True)
    keyexchange_score = models.IntegerField(null=True)
    cipherstrength_score = models.IntegerField(null=True)


### import signals from signals.py (for profile autocreation on user creation)
import signals
