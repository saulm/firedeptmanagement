#coding=utf-8
#from haystack.query import SearchQuerySet
from firedeptmanagement.capitalrelacional.models import RelationalCompany, RelationalPerson
from django.shortcuts import render_to_response
from firedeptmanagement.personal.models import Firefighter
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext

@login_required
def search_related(request):
    query = request.GET.get('query', '')   
    data = {"Firefighter": Firefighter.search(query), "RelationalCompany":RelationalCompany.search(query), "query":query}
    return render_to_response("directorio.html", RequestContext(request, data))
