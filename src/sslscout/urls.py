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

    ### frontpage
    url(r'^$', 'sslscout.views.frontpage'),

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
    url(r'^profile/$', 'sslscout.views.profile_show'),
    url(r'^profile/edit/$', 'sslscout.views.profile_edit'),    

    ### sites
    url(r'^sites/$', 'sslscout.views.site_list'),
    url(r'^sites/add/$', 'sslscout.views.site_add_edit'),
    url(r'^sites/(?P<siteid>\w+)/$', 'sslscout.views.site_details'),
    url(r'^sites/(?P<siteid>\w+)/edit/$', 'sslscout.views.site_add_edit'),
    url(r'^sites/(?P<siteid>\w+)/delete/$', 'sslscout.views.site_delete'),

    ### sitegroups
    url(r'^sitegroups/$', 'sslscout.views.sitegroup_list'),
    url(r'^sitegroups/add/$', 'sslscout.views.sitegroup_add_edit'),
    url(r'^sitegroups/(?P<sitegroupid>\w+)/edit/$', 'sslscout.views.sitegroup_add_edit'),
    url(r'^sitegroups/(?P<sitegroupid>\w+)/delete/$', 'sslscout.views.sitegroup_delete'),    
    url(r'^sitegroups/(?P<sitegroupid>\w+)/$', 'sslscout.views.sitegroup_details'),
    url(r'^sitegroups/(?P<sitegroupid>\w+)/addsite/$', 'sslscout.views.site_add_edit'),
    
    ### check results
    #url(r'^/checkresults/(?P<resultid>\w+)/$', 'sslscout.views.checkresult_details'),

)
