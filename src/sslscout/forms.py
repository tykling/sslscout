from django import forms
from sslscout.models import Profile, SiteGroup

### edit profile form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name','last_name', 'country')


### add sitegroup form
class AddSiteGroupForm(forms.ModelForm):
    class Meta:
        model = SiteGroup
        fields = ('interval_hours','alert')

    def clean(self):
        cleaned_data = super(AddSiteGroupForm, self).clean()
        interval_hours = cleaned_data.get("interval_hours")
        if interval_hours < 24:
            msg = u"The lowest permitted check interval is 24 hours."
            self._errors["interval_hours"] = self.error_class([msg])

        ### remove the invalid field from cleaned_data
        del cleaned_data["interval_hours"]
        
        ### return the cleaned data.
        return cleaned_data


### edit sitegroup form
class EditSiteGroupForm(forms.ModelForm):
    class Meta:
        model = SiteGroup
        fields = ('id','interval_hours','alert')

    def clean(self):
        cleaned_data = super(EditSiteGroupForm, self).clean()
        interval_hours = cleaned_data.get("interval_hours")
        if interval_hours < 24:
            msg = u"The lowest permitted check interval is 24 hours."
            self._errors["interval_hours"] = self.error_class([msg])

        ### remove the invalid field from cleaned_data
        del cleaned_data["interval_hours"]
        
        ### return the cleaned data.
        return cleaned_data


### delete sitegroup form
class DeleteSiteGroupForm(forms.ModelForm):
    class Meta:
        model = SiteGroup
        fields = []

