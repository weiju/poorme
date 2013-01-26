from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

def index(request):
    homeclass = 'navlinksel'
    return render_to_response('index.html', locals())

def about(request):
    aboutclass = 'navlinksel'
    return render_to_response('about.html', locals())

def team(request):
    teamclass = 'navlinksel'
    return render_to_response('team.html', locals())

def contact(request):
    contactclass = 'navlinksel'
    return render_to_response('contact.html', locals())
