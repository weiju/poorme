from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from models import *

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

def communication(request):
    return render_to_response('communication.html', locals())

def input(request):
    symptoms = [s.name for s in Symptom.objects.all()]
    return render_to_response('input.html', locals())
