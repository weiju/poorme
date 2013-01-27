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

    url(r'^$', 'poopreporter.views.index'),
    url(r'^about$', 'poopreporter.views.about'),
    url(r'^team$', 'poopreporter.views.team'),
    url(r'^contact$', 'poopreporter.views.contact'),
    url(r'^communication/(?P<id>[^/]*)$', 'poopreporter.views.communication'),
    url(r'^input$', 'poopreporter.views.input'),
)
