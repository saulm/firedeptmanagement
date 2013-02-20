from firedeptmanagement.personal.models import Firefighter
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.conf import settings

def frontpage(request):
    ff = Firefighter.objects.all()
    data = {}
    data['ff_sample'] = [x for x in ff if x.current_condition_change() and x.current_condition_change().condition_id != settings.BAJ_CONDITION and x.profile_picture][:16]
    return render_to_response('frontpage.html', RequestContext(request, data))
