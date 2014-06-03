from django import forms
from sslscout.models import Profile, SiteGroup, Site
import re

### edit profile form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name','last_name', 'country')


### add/edit sitegroup form
class SiteGroupForm(forms.ModelForm):
    class Meta:
        model = SiteGroup
        fields = ('name','interval_hours','alert')

    def clean(self):
        ### get interval_hours from cleaned_data
        cleaned_data = super(SiteGroupForm, self).clean()
        if 'interval_hours' in cleaned_data:
            interval_hours = cleaned_data.get("interval_hours")

            ### check if interval_hours is numeric
            try:
                temp = float(interval_hours)
            except:
                self._errors["interval_hours"] = self.error_class([u"Invalid input"])
                del cleaned_data["interval_hours"]
                return cleaned_data
            
            ### check if interval_hours is lower than the limit
            if interval_hours < 24:
                self._errors["interval_hours"] = self.error_class([u"The lowest permitted check interval is 24 hours"])
                del cleaned_data["interval_hours"]
                return cleaned_data
            
        ### return the cleaned data.
        return cleaned_data


### delete sitegroup form
class DeleteSiteGroupForm(forms.ModelForm):
    class Meta:
        model = SiteGroup
        fields = []


### add/edit site form
class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ('hostname','sitegroup')

    def clean(self):
        ### get cleaned_data
        cleaned_data = super(SiteForm, self).clean()
        hostname = cleaned_data.get("hostname")

        if hostname[0:8] == "https://":
            self._errors["hostname"] = self.error_class([u"please enter only hostnames, https:// is implied"])
            del cleaned_data["hostname"]
            return cleaned_data

        if hostname[0:8] == "https://":
            self._errors["hostname"] = self.error_class([u"please enter only hostnames, and remember only https on port 443 is supported"])
            del cleaned_data["hostname"]
            return cleaned_data

        if len(hostname) > 255:
            self._errors["hostname"] = self.error_class([u"valid hostnames are limited to 255 characters"])
            del cleaned_data["hostname"]
            return cleaned_data

        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        if not all(allowed.match(x) for x in hostname.split(".")):
            self._errors["hostname"] = self.error_class([u"invalid hostname"])
            del cleaned_data["hostname"]
            return cleaned_data

        ### return the cleaned data.
        return cleaned_data


### delete site form
class DeleteSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = []

