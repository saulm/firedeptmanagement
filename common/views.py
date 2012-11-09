# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from common.models import SuggestionForm
from django.core.mail import send_mail
from django.conf import settings
from common.models import BasePerson
from django.core import serializers
from django.http import HttpResponse

@login_required
def base(request):
    return direct_to_template(request, 'inicio.html')


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
    return direct_to_template(request, 'create_suggestion.html', data)


@login_required
def autocomplete_person(request):
    id_document = request.GET.get("term", "")
    persons = BasePerson.objects.filter(id_document__icontains=id_document).exclude(id_document="")
    return HttpResponse(serializers.serialize('json', persons))


