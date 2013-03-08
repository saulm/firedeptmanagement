from firedeptmanagement.personal.models import Firefighter
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.conf import settings
from django.db.models import Count
from django.db import connection
from ops.models import Service
from datetime import date, datetime, timedelta
from itertools import groupby
from operator import itemgetter
from django.utils.datastructures import SortedDict
from django.http import HttpResponse
import json

def frontpage(request):
    ff = Firefighter.objects.all()
    data = {}
    data['ff_sample'] = [x for x in ff if x.is_active()  and x.profile_picture][:16]

    return render_to_response('frontpage.html', RequestContext(request, data))


def statistics(request):
    truncate_month = connection.ops.date_trunc_sql('month','date')
    summary = Service.objects.filter(date__gt=date(year=2012, month=12, day=31)).extra({'month':truncate_month}).values('month', 'service_type').annotate(Count('service_type')).order_by('-month', 'service_type')
    services_by_month = SortedDict()
    for k, g in  groupby(summary, itemgetter('month')):
        date_formatted = datetime.strptime(k.split(" ", 1)[0], '%Y-%m-%d').strftime("%Y-%m")
        total = 0
        for info in g:
            new_data= {"type":info['service_type'], 'count':info['service_type__count']}
            total+=info['service_type__count']
            if not date_formatted in services_by_month:
                services_by_month[date_formatted] = []
            services_by_month[date_formatted].append(new_data)
        services_by_month[date_formatted].append({"type":"Total:", 'count':total})
    data = {'services_by_month': services_by_month, 'type_legend': Service.SERVICE_TYPE_CHOICES}
    return render_to_response('statistics.html', RequestContext(request, data))


def month_statistics(request, year, month):
    services = Service.objects.filter(date__year=int(year)).filter(date__month=int(month)).values('service_type').annotate(Count('service_type')).order_by('service_type')
    data = {'info': [['Tipo', 'Cantidad']]+[[x['service_type'],x['service_type__count']]  for x in services]}
    return HttpResponse(json.dumps(data))


def month_statistics_detail(request, year, month):
    services = Service.objects.filter(date__year=int(year)).filter(date__month=int(month))
    
    response_times = filter(lambda x: x != None, (service.response_time() for service in services))
    response_time = (sum(response_times, timedelta(0)).seconds/float(len(response_times)))/60.00 if len(response_times) else 0.0
    response_time_text =  ("%.1f" % response_time)+" minutos" if len(response_times) else "No Disponible" 
    
    durations = filter(lambda x: x != None, (service.duration() for service in services))
    
    average_duration = (sum(durations, timedelta(0)).seconds/float(len(durations)))/3600.00 if len(durations) else 0.00
    average_duration_text =  ("%.2f" % average_duration)+" horas" if len(durations) else "No Disponible"
    
    time_in_service = (sum(durations, timedelta(0)).seconds)/3600.00
    time_in_service_text = ("%.2f" % time_in_service)+" horas"
    
    data = {'response_time': response_time_text, 'average_duration': average_duration_text, 'time_in_service': time_in_service_text}
    return HttpResponse(json.dumps(data))
