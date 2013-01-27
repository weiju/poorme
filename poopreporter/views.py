from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
    author = forms.CharField(max_length=200, required=False)
    text = forms.CharField(max_length=1000, required=False)

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        exclude = ['replies', 'status']

    name = forms.CharField(max_length=200, required=False)
    anonymous = forms.BooleanField(required=False)
    status = forms.CharField(max_length=1000, required=False)
    zipcode = forms.CharField(max_length=20, required=False)
    symptoms = forms.TypedMultipleChoiceField(coerce=int, choices=[(s.id, s.name) for s in Symptom.objects.all()])

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

def communication(request, id):
    status = Status.objects.get(id=id)
    replies = status.replies
    print "replies: ", replies.count()
    for reply in replies.all():
        print "reply: ", reply
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save()
            status.replies.add(reply)
            status.save()
            return HttpResponseRedirect('/communication/%s' % str(id))
        else:
            errors = form.errors
    else:
        form = CommentForm()
    return render(request, 'communication.html', locals())

def input(request):
    symptoms = Symptom.objects.all()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            anonymous = form.cleaned_data['anonymous']
            if anonymous:
                name = '(anonymous)'
            status = form.cleaned_data['status']
            mystatus = form.save(commit=False)
            comment = Comment(author=name, text=status)
            comment.save()
            mystatus.status = comment
            mystatus.save()
            return HttpResponseRedirect('/')
        else:
            errors = form.errors
    else:
        print "empty form"
        form = StatusForm()
    return render(request, 'input.html', locals())
