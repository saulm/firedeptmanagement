#coding=utf-8
from ops.forms import ServiceForm, AffectedForm, ServiceVehicleForm, ArrestForm, ArrestPaymentForm, ServiceImageForm
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from ops.models import ServiceVehicle, ServiceAffected, Service, ArrestPayment, ServiceImage
from personal.models import Firefighter
from common.models import BasePerson, TelephoneNumber, PersonTelephoneNumber
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.db import transaction
import json
from datetime import datetime
from django.shortcuts import render

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
    allow_file_upload = request.user.get_profile() in service.complete_crew()
    data = {"service": service, 'allow_file_upload':allow_file_upload}
    
    if allow_file_upload:
        image_upload_form =  ServiceImageForm()
        data["image_upload_form"] = image_upload_form
    
    return render(request, "view_service.html", data)

@login_required
def service_upload_image(request, service_id):
    
    if request.method == 'POST':
        form = ServiceImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = ServiceImage()
            image.service_id = service_id
            image.uploader = request.user.get_profile()
            image.file = form.cleaned_data['image']
            image.save()
            messages.success(request, u'La foto se guardó exitosamente')
        else:
            messages.error(request, u'La foto no se guardó')
    return redirect('view_service', service_id=service_id)
    
    
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
        data['end_time'] = data['end_time'][0:-2]+":"+data['end_time'][-2:]
        data['scene_arrival_time'] = data['scene_arrival_time'][0:-2]+":"+data['scene_arrival_time'][-2:]
        
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
    params['crew_data'] = json.dumps(crew_dict)

    return render_to_response("insert_service.html", RequestContext(request, params))


@login_required
@transaction.commit_on_success
def insert_arrest(request):
    params = {}
    arrest_form = ArrestForm()
    firefighter = request.user.get_profile()
    
    if request.method == 'POST':
        data = request.POST.copy()
        arrest_form = ArrestForm(data)
        if arrest_form.is_valid():
            arrest = arrest_form.save(commit=False)
            arrest.created_by = firefighter
            arrest.arrested = Firefighter.objects.get(id=arrest_form.cleaned_data['arrested'])
            arrest.save()
            messages.success(request, u'El arresto fue guardado exitosamente')
            return redirect(insert_arrest)

    params['arrest_form'] = arrest_form    
    return render_to_response("insert_arrest.html", RequestContext(request, params))


@login_required
@transaction.commit_on_success
def insert_arrest_payment(request):
    params = {}
    arrest_payment_form = ArrestPaymentForm()
    firefighter = request.user.get_profile()
    
    if request.method == 'POST':
        data = request.POST.copy()
        data['start_time_time'] = data['start_time_time'][0:-2]+":"+data['start_time_time'][-2:]
        data['end_time_time'] = data['end_time_time'][0:-2]+":"+data['end_time_time'][-2:]
        
        arrest_payment_form = ArrestPaymentForm(data)
        if arrest_payment_form.is_valid():
            arrest_payment = ArrestPayment()
            arrest_payment.created_by = firefighter
            arrest_payment.start_time = datetime.combine(arrest_payment_form.cleaned_data['start_time_date'], arrest_payment_form.cleaned_data['start_time_time'])
            arrest_payment.end_time = datetime.combine(arrest_payment_form.cleaned_data['end_time_date'], arrest_payment_form.cleaned_data['end_time_time'])
            arrest_payment.payer = Firefighter.objects.get(id=arrest_payment_form.cleaned_data['payer'])
            try:
                arrest_payment.full_clean()
                arrest_payment.save()
                messages.success(request, u'El pago arresto fue guardado exitosamente')
                return redirect(insert_arrest_payment)
            except ValidationError as e:
                messages.error(request, e.message_dict["__all__"][0])
                

    params['arrest_payment_form'] = arrest_payment_form    
    return render_to_response("insert_arrest_payment.html", RequestContext(request, params))
