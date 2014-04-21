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

