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
    interval_hours = models.IntegerField()


### contains all site definitions    
class Site(models.Model):
    sitegroup = models.ForeignKey(SiteGroup)
    hostname = models.CharField(max_length=256)

    def __unicode__(self):
        return u'B%s - %s' % (self.id, self.create_time)


### contains all check results
class SiteChecks(models.Model):
    site = models.ForeighKey(Site)
    datetime = models.DateTimeField(auto_now_add=True)
    result_html = models.TextField()

    
### import signals from signals.py (for profile autocreation on user creation)
import signals
