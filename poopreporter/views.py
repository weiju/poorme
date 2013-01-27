from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from models import *

class StatusForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    anonymous = forms.BooleanField(required=False)
    status = forms.CharField(max_length=1000, required=False)
    zipcode = forms.CharField(max_length=20, required=False)

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
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            anonymous = form.cleaned_data['anonymous']
            status = form.cleaned_data['status']
            zipcode = form.cleaned_data['zipcode']
            print "name: ", name
            print "anonymous: ", anonymous
            print "status: ", status
            print "zipcode: ", zipcode

            return HttpResponseRedirect('/')
    else:
        print "empty form"
        form = StatusForm()
    return render(request, 'input.html', locals())
