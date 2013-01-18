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
from django.db import transaction
import simplejson

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
def view_service(request, service_id):
    service = Service.objects.get(id=service_id)
    return render_to_response("view_service.html", RequestContext(request, {"service": service}))

@login_required
@transaction.commit_on_success
def insert_service(request):
    params = {}
    AffectedFormSet = formset_factory(AffectedForm, extra=0)
    VehiclesFormSet = formset_factory(ServiceVehicleForm, extra=1)
    firefighter = request.user.get_profile()
    service_form = ServiceForm()
    crew_dict = {}

    if request.method == 'POST':
        data = request.POST.copy()
        data['time'] = data['time'][0:-2]+":"+data['time'][-2:]
        
        service_form = ServiceForm(data)
        affected_formset = AffectedFormSet(data, prefix='affected')
        vehicles_formset = VehiclesFormSet(data, prefix='vehicles')
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
                    if af.cleaned_data["id_document"]:
                        person, _ = BasePerson.objects.get_or_create(id_document=af.cleaned_data["id_document"])
                    else:
                        person = BasePerson()
                    person.first_name = af.cleaned_data['first_name']
                    person.first_name_2 = af.cleaned_data['first_name_2']
                    person.last_name = af.cleaned_data['last_name']
                    person.last_name_2 = af.cleaned_data['last_name_2']
                    person.gender = af.cleaned_data['gender']
                    if af.cleaned_data["primary_email"]:
                        person.primary_email = af.cleaned_data["primary_email"]

                    person.save()
                    if af.cleaned_data["phone_code"] and af.cleaned_data["phone_number"]:
                        telephone = TelephoneNumber(code=af.cleaned_data["phone_code"],
                                                    number=af.cleaned_data["phone_number"])
                        telephone.save()
                        PersonTelephoneNumber(person=person,type='O',
                                              telephone_number=telephone).save()

                    s_affected = ServiceAffected(person_affected=person,
                                                 notes=af.cleaned_data["notes"],
                                                 type=af.cleaned_data["type"])
                    s_affected.save()
                    service.affected.add(s_affected)
            messages.success(request, u'El servicio fue guardado exitosamente')
            return redirect(list_services)
        else:
            crew_ids_str = ""
            for k, v in data.iteritems():
                if "crew_ids" in k and v!="":
                    crew_ids_str = crew_ids_str+","+v
            crew_ids = [x for x in crew_ids_str.split(",") if x!='']

#            import ipdb;ipdb.set_trace()
            crew = Firefighter.objects.filter(id__in=crew_ids)
            for member in crew:
                crew_dict[member.id] = str(member)
    else:
        affected_formset = AffectedFormSet(prefix='affected')
        vehicles_formset = VehiclesFormSet(prefix='vehicles')
        
    params['form'] = service_form
    params['affected'] = affected_formset
    params['vehicles'] =  vehicles_formset
    params['media'] = service_form.media
    params['ff'] = firefighter
    params['crew_data'] = simplejson.dumps(crew_dict)

    return render_to_response("insert_service.html", RequestContext(request, params))
