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
    sitegroup = models.ForeignKey(SiteGroup,related_name="sites")
    hostname = models.CharField(max_length=256)
    def __unicode__(self):
        return self.hostname


### defines the different engines available
class CheckEngine(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    checkurl = models.CharField(max_length=200)
    cacheclearurl = models.CharField(max_length=200)
    engineclass = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    def __unicode__(self):
        return self.name


### contains the running and finished checks of hostnames
class SiteCheck(models.Model):
    hostname = models.CharField(max_length=256)
    engine = models.ForeignKey(CheckEngine)
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True)
    def __unicode__(self):
        return "%s - %s: %s" % (self.hostname, self.engine, self.start_time)
    class Meta:
        ordering = ['-finish_time']

        
### log output from sitechecks
class SiteCheckLog(models.Model):
    sitecheck = models.ForeignKey(SiteCheck,related_name="checklogs")
    datetime = models.DateTimeField(auto_now_add=True)
    logentry = models.CharField(max_length=1000)
    def __unicode__(self):
        return "%s - %s: %s" % (self.sitecheck.id, self.datetime, self.logentry)


### requestlog
class RequestLog(models.Model):
    sitecheck = models.ForeignKey(SiteCheck,related_name="requestlogs")
    datetime = models.DateTimeField(auto_now_add=True)
    uuid = UUIDField()
    request_url = models.CharField(max_length=1000)
    request_headers = models.TextField()
    request_body = models.TextField(null=True)
    response_code = models.IntegerField(null=True)
    response_headers = models.TextField(null=True)
    response_body = models.TextField(null=True)
    def __unicode__(self):
        return "%s - %s: %s" % (self.sitecheck.id, self.datetime, self.request_url)
    class Meta:
        ordering = ['-datetime']


### contains the results of a sitecheck, can contain multiple entries 
### per sitecheck if a hostname resolves to multiple IP addresses
class SiteCheckResult(models.Model):
    sitecheck = models.ForeignKey(SiteCheck,related_name='results')
    serverip = models.GenericIPAddressField(unpack_ipv4=True,null=True,blank=True)
    overall_rating = models.CharField(max_length=2,null=True,blank=True)
    certificate_score = models.IntegerField(null=True,blank=True)
    protocolsupport_score = models.IntegerField(null=True,blank=True)
    keyexchange_score = models.IntegerField(null=True,blank=True)
    cipherstrength_score = models.IntegerField(null=True,blank=True)
    error_string = models.TextField(null=True,blank=True)
    def __unicode__(self):
        return "%s - %s: %s" % (self.sitecheck.hostname, self.sitecheck.finish_time, self.overall_rating)


### import signals from signals.py (for profile autocreation on user creation)
import signals
