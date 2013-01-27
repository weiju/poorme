from django.http import HttpResponse
from django.utils import simplejson
from poopreporter.models import Status, Zipcode, Symptom

def statuses(request):
    data = build_statuses()
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def build_statuses():
    data = []
    query = Status.objects.all()
    for status in query:
        zip_query = Zipcode.objects.filter(zipcode=status.zipcode)
        if zip_query.count() > 0:
            status_data = {
                'name': status.name, 
                'status': status.status.text, 
                'url': '/communication/' + str(status.id), 
                'latitude': str(zip_query[0].latitude),
                'longitude': str(zip_query[0].longitude),
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
        zip_query = Zipcode.objects.filter(zipcode=status.zipcode)
        if zip_query.count():
            symptoms = status.symptoms.all()
            for symptom in symptoms:
                symptom_data = {
                    'name': symptom.name,
                    'latitude': str(zip_query[0].latitude),
                    'longitude': str(zip_query[0].longitude),
                }

                name = str(symptom.name)
                if data.has_key(name):
                    data[name] += [symptom_data]
                else:
                    data[name] = [symptom_data]
    return data

def build_symptom_list():
    data = []
    query = Symptom.objects.all()
    for symptom in query:
        data.append(symptom.name)
    return data

def statuses_and_symptoms(request):
    statuses = build_statuses()
    symptoms = build_symptoms()
    symptom_list = build_symptom_list()
    data = {'statuses': statuses, 'symptoms': symptoms, 'symptom_list': symptom_list}
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
