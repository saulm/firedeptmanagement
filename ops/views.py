from ops.forms import ServiceForm, AffectedForm, ServiceVehicleForm
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from ops.models import ServiceVehicle, ServiceAffected, Service
from personal.models import Firefighter
from common.models import BasePerson, TelephoneNumber, PersonTelephoneNumber
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def list_services(request):
    services_qs = Service.objects.all()
    paginator = Paginator(services_qs, 15)
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        services = paginator.page(1)
    except EmptyPage:
        services = paginator.page(paginator.num_pages)

    return render_to_response("list_services.html", RequestContext(request, {"services": services, "paginator": paginator}))


@login_required
def insert_service(request):
    params = {}
    affected_formset = formset_factory(AffectedForm, extra=10)
    vehicles_formset = formset_factory(ServiceVehicleForm, extra=5)
    firefighter = request.user.get_profile()
    service_form = ServiceForm()

    if request.method == 'POST':
        data = request.POST.copy()
        service_form = ServiceForm(data)
        affected_formset = affected_formset(data)
        vehicles_formset = vehicles_formset(data)

        if service_form.is_valid() and affected_formset.is_valid() and vehicles_formset.is_valid():
            service = service_form.save()
            service.created_by = firefighter
            service.save()

            for vf in vehicles_formset.forms:
                if "lead" in vf.cleaned_data:
                    s_vehicle = ServiceVehicle()
                    s_vehicle.service = service
                    s_vehicle.lead = Firefighter.objects.get(id=vf.cleaned_data['lead'])
                    s_vehicle.vehicle = vf.cleaned_data['vehicle']
                    if vf.cleaned_data['driver']:
                        s_vehicle.driver = Firefighter.objects.get(id=vf.cleaned_data['driver'])

                    s_vehicle.save()

                    for crew_id in vf.cleaned_data['crew_ids'].split(","):
                        if crew_id != "":
                            s_vehicle.crew.add(Firefighter.objects.get(id=crew_id))

            for af in affected_formset.forms:
                if 'first_name' in af.cleaned_data:
                    person, _ = BasePerson.objects.get_or_create(id_document=af.cleaned_data["id_document"])
                    person.first_name = af.cleaned_data['first_name']
                    person.first_name_2 = af.cleaned_data['first_name_2']
                    person.last_name = af.cleaned_data['last_name']
                    person.last_name_2 = af.cleaned_data['last_name_2']
                    person.gender = af.cleaned_data['gender']
                    if af.cleaned_data["primary_email"]:
                        person.primary_email = af.cleaned_data["primary_email"]

                    person.save()

                    telephone = TelephoneNumber(code=af.cleaned_data["phone_code"],
                                                number=af.cleaned_data["phone_number"])
                    telephone.save()
                    PersonTelephoneNumber(person=person,
                                          type='O',
                                          telephone_number=telephone).save()

                    s_affected = ServiceAffected(person_affected=person,
                                                 notes=af.cleaned_data["notes"],
                                                 type=af.cleaned_data["type"])
                    s_affected.save()
                    service.affected.add(s_affected)
            messages.success(request, u'El servicio fue guardado exitosamente')
            return redirect(list_services)

    params['form'] = service_form
    params['affected'] = affected_formset
    params['vehicles'] = vehicles_formset
    params['media'] = service_form.media
    params['ff'] = firefighter

    return render_to_response("insert_service.html", RequestContext(request, params))
