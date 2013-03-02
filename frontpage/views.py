from firedeptmanagement.personal.models import Firefighter
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.conf import settings

def frontpage(request):
    ff = Firefighter.objects.all()
    data = {}
    data['ff_sample'] = [x for x in ff if x.is_active()  and x.profile_picture][:16]
    return render_to_response('frontpage.html', RequestContext(request, data))

#Service.objects.extra({'month':truncate_month}).values('month', 'service_type').annotate(Count('service_type')).order_by('-month')
#Service.objects.extra({'month':truncate_month}).values('month').annotate(Count('id')).order_by('-month')Out[28]: [{'id__count': 28, 'month': datetime.datetime(2013, 2, 1, 0, 0)}, {'id__count': 45, 'month': datetime.datetime(2013, 1, 1, 0, 0)}, {'id__count': 7, 'month': datetime.datetime(2012, 12, 1, 0, 0)}, {'id__count': 18, 'month': datetime.datetime(2012, 11, 1, 0, 0)}, {'id__count': 14, 'month': datetime.datetime(2012, 10, 1, 0, 0)}, {'id__count': 7, 'month': datetime.datetime(2012, 9, 1, 0, 0)}, {'id__count': 6, 'month': datetime.datetime(2012, 8, 1, 0, 0)}, {'id__count': 8, 'month': datetime.datetime(2012, 7, 1, 0, 0)}, {'id__count': 4, 'month': datetime.datetime(2012, 6, 1, 0, 0)}, {'id__count': 3, 'month': datetime.datetime(2012, 5, 1, 0, 0)}, {'id__count': 1, 'month': datetime.datetime(2012, 3, 1, 0, 0)}]
