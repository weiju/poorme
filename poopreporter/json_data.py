from django.http import HttpResponse
from django.utils import simplejson
from poopreporter.models import Status, Symptom
from zipmap import ZIPCODES


def statuses(request):
    data = build_statuses()
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def build_statuses():
    data = []
    query = Status.objects.all()
    for status in query:
        if status.zipcode in ZIPCODES:
            latitude, longitude = ZIPCODES[status.zipcode]
            status_data = {
                'name': status.name,
                'status': status.status.text,
                'url': '/communication/' + str(status.id),
                'latitude': str(latitude),
                'longitude': str(longitude),
            }
            data.append(status_data)
    return data


def symptoms(request):
    data = build_symptoms()
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def build_symptoms():
    data = {}
    query = Status.objects.all()
    for status in query:
        if status.zipcode in ZIPCODES:
            latitude, longitude = ZIPCODES[status.zipcode]
            symptoms = status.symptoms.all()
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
