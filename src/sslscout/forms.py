from django import forms
from sslscout.models import Profile

### edit profile form
class ProfileForm(forms.ModelForm):
  class Meta:
      model = Profile
      fields = ('first_name','last_name', 'country')
