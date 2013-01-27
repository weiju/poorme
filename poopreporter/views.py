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
    status = forms.CharField(max_length=1000, required=True)
    zipcode = forms.CharField(max_length=20, required=True)
    symptoms = forms.TypedMultipleChoiceField(coerce=int, choices=[(s.id, s.name) for s in Symptom.objects.all()])
    wishlist = forms.TypedMultipleChoiceField(required=False, coerce=int, choices=[(s.id, s.name) for s in Stuff.objects.all()])

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
    wishlist = status.wishlist
    print "replies: ", replies.count()
    print "wishes: ", wishlist.count()

    for wish in wishlist.all():
        print "wish: ", wish

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
    stuffs = Stuff.objects.all()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            anonymous = form.cleaned_data['anonymous']
            wishes = form.cleaned_data['wishlist']
            syms = form.cleaned_data['symptoms']
            print "wishes: ", wishes
            print "symptoms: ", syms

            if anonymous:
                name = '(anonymous)'
            status = form.cleaned_data['status']
            mystatus = form.save(commit=False)
            comment = Comment(author=name, text=status)
            comment.save()
            mystatus.status = comment
            mystatus.save()
            form.save_m2m()
            return HttpResponseRedirect('/communication/%d' % mystatus.id)
        else:
            errors = form.errors
    else:
        print "empty form"
        form = StatusForm()
    return render(request, 'input.html', locals())
