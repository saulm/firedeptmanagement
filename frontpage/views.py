from firedeptmanagement.personal.models import Firefighter
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def frontpage(request):
    ff = Firefighter.objects.all()
    data = {"ff_sample":[f for f in ff if f.profile_picture][:16]}
    return render_to_response('frontpage.html', RequestContext(request, data))
