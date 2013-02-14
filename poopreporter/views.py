from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from social_auth.models import UserSocialAuth


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name', 'zipcode', 'symptoms', 'wishlist']

    anonymous = forms.BooleanField(required=False)
    status = forms.CharField(max_length=1000, required=True)
    symptoms = forms.TypedMultipleChoiceField(
        coerce=int, choices=[(s.id, s.name) for s in Symptom.objects.all()])
    wishlist = forms.TypedMultipleChoiceField(
        required=False, coerce=int, choices=[(s.id, s.name)
                                             for s in Stuff.objects.all()])


def index(request):
    homeclass = 'selected'
    return render_to_response('index.html', locals(), RequestContext(request))


def about(request):
    aboutclass = 'selected'
    return render_to_response('about.html', locals(), RequestContext(request))


def team(request):
    teamclass = 'selected'
    return render_to_response('team.html', locals(), RequestContext(request))


def contact(request):
    contactclass = 'selected'
    return render_to_response('contact.html', locals(), RequestContext(request))


def communication(request, id):
    status = Status.objects.get(id=id)
    replies = status.replies
    wishlist = status.wishlist

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
    return render(request, 'communication.html', locals(), RequestContext(request))


def input(request):
    symptoms = Symptom.objects.all().order_by('name')
    stuffs = Stuff.objects.all()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            anonymous = form.cleaned_data['anonymous']
            wishes = form.cleaned_data['wishlist']
            syms = form.cleaned_data['symptoms']

            status = form.cleaned_data['status']
            mystatus = form.save(commit=False)
            comment = Comment(author=name, text=status)
            comment.save()
            # check whether we are anonymous
            if anonymous or len(name.strip()) == 0:
                mystatus.name = 'Anonymous'

            mystatus.status = comment
            mystatus.save()
            form.save_m2m()
            return HttpResponseRedirect('/communication/%d' % mystatus.id)
        else:
            errors = form.errors
    else:
        print "empty form"
        form = StatusForm()
    return render(request, 'input.html', locals(), RequestContext(request))

def profile(request):
    cat_var = 55
    print "USER:", request.user
    instance = UserSocialAuth.objects.filter(provider='facebook').get()
    print instance.tokens
    profile_pic = "http://graph.facebook.com/%s/picture?type=large" % (request.user)
    return render_to_response('profile.html', locals(), RequestContext(request))


class UserForm(forms.ModelForm):
    class Meta:
        model = User  

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username,
                                password=password)
            login(request, user)
            return HttpResponseRedirect("/accounts/profile/")
        return render(request,
                      'register.html',
                      { 'form' : user_form })

    else:
        uf = UserCreationForm()
    return render_to_response('register.html', {'form': uf}, RequestContext(request))
