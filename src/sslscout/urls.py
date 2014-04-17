from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_complete, password_reset_confirm, password_change, password_change_done
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import ActivationView, RegistrationView

from sslscout.forms import ProfileForm

admin.autodiscover()

urlpatterns = patterns('',
    ### admin site
    url(r'^admin/', include(admin.site.urls)),

    ### static pages
    url(r'^$', 'sslscout.views.staticpage',{'page': 'frontpage.html'}),

    ### auth and pw stuff
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': '/accounts/login/'}, name='logout'),
    url(r'^accounts/password_change/$', password_change, {'template_name': 'registration/password_change.html'}, name='password_change'),
    url(r'^accounts/password_change_done/$', password_change_done, {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
    url(r'^accounts/password_reset/$', password_reset, {'template_name': 'registration/password_reset.html'}, name='password_reset'),
    url(r'^accounts/password_reset_done/$', password_reset_done, {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^accounts/password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^accounts/password_reset_complete/$', password_reset_complete, {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/profile/', permanent=True), name='profile'),

    ### registration stuff
    url(r'^accounts/activate/complete/$', TemplateView.as_view(template_name='registration/activation_complete.html'), name='registration_activation_complete'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),name='registration_register'),
    url(r'^register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'), name='registration_complete'),
    url(r'^register/closed/$', TemplateView.as_view(template_name='registration/registration_closed.html'), name='registration_disallowed'),
    
    ### profile stuff
    url(r'^profile/$', 'sslscout.views.profile'),
    url(r'^profile/edit/$', 'sslscout.views.profile_edit'),    

    ### site and sitegroup related stuff
    #url(r'^sites/$', 'sslscout.views.sites'),
    #url(r'^sites/add/$', 'sslscout.views.add_site'),
    #url(r'^sites/edit/(?P<siteid>\w+)/$', 'sslscout.views.edit_site'),
    #url(r'^sites/delete/(?P<siteid>\w+)/$', 'sslscout.views.delete_site'),
    #url(r'^sitegroups/$', 'sslscout.views.sitegroups'),
    #url(r'^sitegroups/add/$', 'sslscout.views.add_sitegroup'),
    #url(r'^sitegroups/edit/(?P<siteid>\w+)/$', 'sslscout.views.edit_sitegroup'),
    #url(r'^sitegroups/delete/(?P<siteid>\w+)/$', 'sslscout.views.delete_sitegroup'),    
)
