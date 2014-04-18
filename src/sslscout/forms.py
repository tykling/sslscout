from django import forms
from sslscout.models import Profile, SiteGroup

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
        cleaned_data = super(SiteGroupForm, self).clean()

        ### check that interval_hours is 24 or more
        interval_hours = cleaned_data.get("interval_hours")
        if interval_hours < 24:
            self._errors["interval_hours"] = self.error_class([u"The lowest permitted check interval is 24 hours."])
            del cleaned_data["interval_hours"]
        
        ### return the cleaned data.
        return cleaned_data

### delete sitegroup form
class DeleteSiteGroupForm(forms.ModelForm):
    class Meta:
        model = SiteGroup
        fields = []

