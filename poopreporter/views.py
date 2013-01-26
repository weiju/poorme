from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

def index(request):
    return render_to_response('index.html', locals())

def about(request):
    return render_to_response('about.html', locals())
