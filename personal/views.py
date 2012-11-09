#coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from personal.models import Firefighter
from personal.forms import PersonPhoneForm, PartialFirefighterForm
from django.template.context import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from utils.serialization import get_values
import simplejson


@login_required
def user_profile(request, ff_id=None):
    params = {}
    if ff_id:
        firefighter = Firefighter.objects.get(id=ff_id)
    else:
        firefighter = request.user.get_profile()

    params["firefighter"] = firefighter
    return render_to_response("perfil.html", RequestContext(request, params))


@login_required
def view_cnb_form(request, ff_id):
    firefighter = Firefighter.objects.get(id=ff_id)
    params = {"ff": firefighter}
    return render_to_response("planilla_cnb.html", RequestContext(request, params))


@login_required
def change_profile_get(request):
    params = {}
    firefighter = request.user.get_profile()
    form = PersonPhoneForm()
    profile_form = PartialFirefighterForm(instance=firefighter)

    bound_forms = []
    for person_phone in firefighter.persontelephonenumber_set.all():
        data = {
                'id': person_phone.id,
                'type': person_phone.type,
                'code': person_phone.telephone_number.code,
                'number': person_phone.telephone_number.number
                }
        bound_forms.append(PersonPhoneForm(data))

    params['bound_forms'] = bound_forms
    params['new_form'] = form
    params['profile_form'] = profile_form

    return render_to_response("change_profile.html", RequestContext(request, params))


@login_required
def change_profile(request):
    if request.method == "POST":
        firefighter = request.user.get_profile()
        profile_form = PartialFirefighterForm(request.POST, request.FILES, instance=firefighter)
        if profile_form.is_valid():
            profile_form.save()
    return redirect(change_profile_get)


@login_required
def change_phone(request):
    firefighter = request.user.get_profile()
    form = PersonPhoneForm()
    if request.method == "POST":
        form = PersonPhoneForm(request.POST)
        if form.is_valid():
            messages.success(request, u'Los cambios fueron guardados exitosamente')
            form.save(firefighter)
        else:
            messages.error(request, u'Existen errores en el formulario, chequea que estes usando el formato correcto (código: 0212, número: 1231212)')
    return redirect(change_profile_get)


@login_required
def delete_phone(request, phone_id):
    firefighter = request.user.get_profile()
    firefighter.persontelephonenumber_set.get(id=phone_id).delete()
    return redirect(change_profile_get)


@login_required
def autocomplete_firefighter(request):
    term = request.GET.get("term", "")
    ffs = Firefighter.search(term)
    return HttpResponse(simplejson.dumps([get_values(x) for x in ffs]))
