from django.http import HttpResponse
from django.utils import simplejson
from poopreporter.models import *
from zipmap import ZIPCODES


def statuses(request):
    data = build_statuses()
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def latlong(update):
    return ZIPCODES[update.episode.zipcode]

def build_statuses():
    data = []
    query = Episode.objects.all()
    for episode in query:
        if episode.zipcode in ZIPCODES:
            latitude, longitude = ZIPCODES[episode.zipcode]
            first_comment = LoggedInComment.objects.filter(episode=episode)[0]
            update_data = {
                'name': episode.user.first_name,
                'status': first_comment.text,
                'url': '/episode/' + str(episode.id),
                'latitude': str(latitude),
                'longitude': str(longitude),
            }
            data.append(update_data)
    return data


def symptoms(request):
    data = build_symptoms()
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def build_symptoms():
    data = {}
    query = Update.objects.all()
    for update in query:
        if update.episode.zipcode in ZIPCODES:
            latitude, longitude = latlong(update)
            symptoms = update.symptoms.all()
            for symptom in symptoms:
                symptom_data = {
                    'name': symptom.name,
                    'latitude': str(latitude),
                    'longitude': str(longitude),
                }
                name = str(symptom.name)
                if name in data:
                    data[name] += [symptom_data]
                else:
                    data[name] = [symptom_data]
    return data


def build_symptom_list():
    query = Symptom.objects.all()
    return sorted([symptom.name for symptom in query])


def statuses_and_symptoms(request):
    statuses = build_statuses()
    symptoms = build_symptoms()
    symptom_list = build_symptom_list()
    data = {'statuses': statuses, 'symptoms': symptoms,
            'symptom_list': symptom_list}
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
