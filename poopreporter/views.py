from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from social_auth.models import UserSocialAuth

  
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


def profile(request):
    #auth_token = UserSocialAuth.objects.filter(provider='facebook').get().tokens
    episodes = Episode.objects.filter(user=request.user).order_by('-started')
    profile_pic = "http://graph.facebook.com/%s/picture?type=large" % (request.user)
    return render_to_response('profile.html', locals(), RequestContext(request))

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = ['symptoms']
        
    symptom_choices= [(s.id, s.name) for s in Symptom.objects.all()]
    symptoms = forms.MultipleChoiceField(choices=symptom_choices, required=True, widget=forms.CheckboxSelectMultiple(), label='Select your symptoms') 


class CommentForm(forms.ModelForm):
    class Meta:
        model = LoggedInComment
        fields = ['text']
        
    text = forms.CharField(max_length=1000, widget=forms.Textarea)

class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ['zipcode', 'wishlist']
        
    wishlist_choices = [(s.id, s.name) for s in Stuff.objects.all()]
    wishlist = forms.MultipleChoiceField(choices=wishlist_choices, required=False, widget=forms.CheckboxSelectMultiple(), label='What would help you feel better?') 
    
def updateSymptoms(request, id):
    episode = Episode.objects.get(id=id)
    
    if request.method == 'POST':
        update_form = UpdateForm(request.POST)
        
        if update_form.is_valid(): 
            update = update_form.save(commit=False)
            update.episode = episode
            update.save()
            update_form.save_m2m()
        return HttpResponseRedirect('/episode/%d' % int(id))
            
def addComment(request, id):
    episode = Episode.objects.get(id=id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid(): 
            comment = comment_form.save(commit=False)
            comment.episode = episode
            comment.user = request.user
            comment.save()
        return HttpResponseRedirect('/episode/%d' % int(id))


def episode(request, id):
    episode = Episode.objects.get(id=id)
        
    updates = Update.objects.filter(episode=episode).order_by('time')
    comments = LoggedInComment.objects.filter(episode=episode).order_by('time')[1:]
    last_symptoms = map(lambda x: x.pk, updates[len(updates)-1].symptoms.all())
    form = UpdateForm()
    form.fields['symptoms'].initial = last_symptoms
    
    comment_form = CommentForm()
    
    name = episode.user.first_name
    status = episode.status
    wishlist = episode.wishlist
    return render_to_response('episode.html', locals(), RequestContext(request))


def input(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
        
    if request.method == 'POST':    
        print "POST"
        episode_form = EpisodeForm(request.POST, instance=Episode())
        update_form = UpdateForm(request.POST, instance=Update())
        text_form = CommentForm(request.POST, instance=LoggedInComment())
        if episode_form.is_valid() and update_form.is_valid() and text_form.is_valid():
            episode = episode_form.save(commit=False)
            print episode
            episode.user = request.user
            episode.save()
            episode_form.save_m2m()
            
            update = update_form.save(commit=False)
            print update
            update.episode = episode
            update.save()
            update_form.save_m2m()
            
            comment = text_form.save(commit=False)
            print comment
            comment.episode = episode
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect('/accounts/profile/')
        else:
            episode_errors = episode_form.errors
            text_errors = text_form.errors
            update_errors = update_form.errors
                
    else:
        episode_form = EpisodeForm(instance=Episode())
        update_form = UpdateForm(instance=Update())
        text_form = CommentForm(instance=LoggedInComment())
    
    return render_to_response('sick.html', locals(), RequestContext(request))



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
