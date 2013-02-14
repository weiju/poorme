from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'poopreporter.views.home', name='home'),
    # url(r'^poopreporter/', include('poopreporter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls')),

    url(r'^accounts/login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    url(r'^accounts/profile/$', 'poopreporter.views.profile' ),
    url(r'^accounts/register/$', 'poopreporter.views.register' ),

    url(r'^$', 'poopreporter.views.index'),
    url(r'^about$', 'poopreporter.views.about'),
    url(r'^team$', 'poopreporter.views.team'),
    url(r'^contact$', 'poopreporter.views.contact'),
    url(r'^communication/(?P<id>[^/]*)$', 'poopreporter.views.communication'),
    url(r'^input$', 'poopreporter.views.input'),

    url(r'^statuses$', 'poopreporter.json_data.statuses'),
    url(r'^symptoms$', 'poopreporter.json_data.symptoms'),
    url(r'^data$', 'poopreporter.json_data.statuses_and_symptoms'),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': '/static/images/favicon.ico'}),

    url(r'', include('social_auth.urls')),
)
