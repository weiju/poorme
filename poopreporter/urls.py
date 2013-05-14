from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'poopreporter.views.index'),
    url(r'^about$', 'poopreporter.views.about'),
    url(r'^team$', 'poopreporter.views.team'),
    url(r'^contact$', 'poopreporter.views.contact'),


    url(r'^statuses$', 'poopreporter.json_data.statuses'),
    url(r'^symptoms$', 'poopreporter.json_data.symptoms'),
    url(r'^data$', 'poopreporter.json_data.statuses_and_symptoms'),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': '/static/images/favicon.ico'}),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    url(r'^accounts/profile/$', 'poopreporter.views.profile' ),
    url(r'^accounts/register/$', 'poopreporter.views.register' ),
    
    url(r'^episode/(?P<id>[^/]*)/$', 'poopreporter.views.episode' ),
    url(r'^input/$', 'poopreporter.views.input' ),
    url(r'^updatesymptoms/(?P<id>[^/]*)/$', 'poopreporter.views.updateSymptoms' ),
    url(r'^addcomment/(?P<id>[^/]*)/$', 'poopreporter.views.addComment' ),
    
    
    url(r'', include('social_auth.urls')),
)
