from django.http import HttpResponse
from django.utils import simplejson
from poopreporter.models import Status, Zipcode

def statuses(request):
    data = []
    query = Status.objects.all()
    for status in query:
        zip_query = Zipcode.objects.filter(zipcode=status.zipcode)[0]
        
        status_data = {
            'name': status.name, 
            'status': status.status.text, 
            'url': 'http://google.com', 
            'latitude': str(zip_query.latitude),
            'longitude': str(zip_query.longitude),
        }
        data.append(status_data)

    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def symptoms(request):
    data = {}
    query = Status.objects.all()
    for status in query:
        zip_query = Zipcode.objects.filter(zipcode=status.zipcode)[0]
        symptoms = status.symptoms.all()
        for symptom in symptoms:
            symptom_data = {
                'name': symptom.name,
                'latitude': str(zip_query.latitude),
                'longitude': str(zip_query.longitude),
            }
            
            name = str(symptom.name)
            if data.has_key(name):
                data[name] += [symptom_data]
            else:
                data[name] = [symptom_data]

    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
