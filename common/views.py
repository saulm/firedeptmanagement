# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from common.models import SuggestionForm
from django.core.mail import send_mail
from django.conf import settings
from common.models import BasePerson
from django.core import serializers
from django.http import HttpResponse
from datetime import date
from personal.models import Firefighter
from ops.models import Service
import json

@login_required
def base(request):
    data = {}
    f = Firefighter.objects.filter(birth_date__month=date.today().month).order_by("birth_date")
    data['birthdays'] = [x for x in f if x.current_condition_change() and x.current_condition_change().condition_id != settings.BAJ_CONDITION]
    data['last_services'] = Service.objects.filter()[:10]
    services_locs = []
    for service in data['last_services']:
        if service.map_location:
            service_locs.append({'id':str(service.id), 'loc':service.map_location, 'lat':float(service.map_location.split(",")[0]), 'lng':float(service.map_location.split(",")[1])})            
    data['last_services_locations'] = json.dumps(services_locs)
    
    return render(request, 'inicio.html', data)

@login_required
def create_suggestion(request):
    data = {}
    if request.method == "POST":
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save()
            send_mail(settings.SUGGESTION_MAIL_SUBJECT,
                      suggestion.text,
                      settings.SUGGESTION_MAIL_FROM,
                      settings.SUGGESTION_MAIL_TO, fail_silently=True)
            data['thanks'] = True
            form = SuggestionForm()
    else:
        form = SuggestionForm()
    data['form'] = form
    return render(request, 'create_suggestion.html', data)


@login_required
def autocomplete_person(request):
    id_document = request.GET.get("term", "")
    persons = BasePerson.objects.filter(id_document__icontains=id_document).exclude(id_document="")
    return HttpResponse(serializers.serialize('json', persons))
