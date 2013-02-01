#coding=utf-8
from django.forms.models import ModelForm
from ops.models import Service, Vehicle, ServiceAffected, Arrest, ArrestPayment
from django.db import models
from django.core import validators
from common.models import BasePerson
from django import forms
from django.forms.widgets import SplitDateTimeWidget

def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class': 'datePicker input-xlarge',
                                       'readonly': 'true',
                                       "placeholder": "dd/mm/aa"})
    elif isinstance(f, models.TextField):
        formfield.widget.attrs.update({'style': 'width:600px;'})
    elif isinstance(f, models.CharField):
        formfield.widget.attrs.update({'class': 'input-xlarge'})
    elif isinstance(f, models.TimeField):
        formfield.widget.format = '%H:%M'
        formfield.widget.attrs.update({'class': 'input-xlarge'})

    return formfield


class ServiceForm(ModelForm):
    formfield_callback = make_custom_datefield

    class Meta:
        model = Service
        exclude = ("affected",)


class ServiceVehicleForm(forms.Form):
    lead_select = forms.CharField(label=u'Jefe de Comisión', required=True,
                                  help_text=u"Asegurate de Seleccionar el Jefe de la lista que se despliega!")
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all(),
                                     label="Unidad",
                                     help_text=u"No selecciones nada si la comisión fue sin unidad",
                                     required=False)
    lead = forms.CharField(widget=forms.HiddenInput, required=True)
    driver_select = forms.CharField(label=u'Conductor', required=False)
    driver = forms.CharField(widget=forms.HiddenInput, required=False)
    crew_select = forms.CharField(label=u'Acompañante',
                                  help_text=u"Escribe el nombre, carnet, iniciales o nombre de usuario del personal, seleccionalo de la lista para agregarlo",
                                  required=False)
    crew_ids = forms.CharField(widget=forms.HiddenInput, required=False)


class AffectedForm(ModelForm):
    phone_code = forms.CharField(label=u'Código Telefono',
                                 validators=[validators.MaxLengthValidator(4),
                                             validators.RegexValidator(regex="\d\d\d\d")],
                                 help_text='Ejemplo: 0416 ó 0414 ó 0212', required=False)
    phone_number = forms.CharField(label=u'Número Telefono',
                                   validators=[validators.MaxLengthValidator(7),
                                               validators.RegexValidator(regex="\d\d\d\d\d\d\d")],
                                   help_text='El resto del número Ejemplo: 9063909', required=False)
    notes = forms.CharField(label="Notas/Tratamiento", widget=forms.Textarea(),
                            required=False)
    type = forms.CharField(label="Tipo", widget=forms.Select(choices=ServiceAffected.AFFECTED_TYPE_CHOICES))

    class Meta:
        model = BasePerson
        exclude = ('alternate_email')
        fields = ('id_document', 'first_name', 'first_name_2', 'last_name',
                  'last_name_2', 'gender', 'primary_email', 'phone_code',
                  'phone_number', 'notes')

def make_custom_datefield_for_arrest(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class': 'datePicker',
                                       'readonly': 'true',
                                       "placeholder": "dd/mm/aa"})
    elif isinstance(f, models.TimeField):
        formfield.widget.format = '%H%M'
    return formfield


class ArrestForm(ModelForm):
    arrested_select = forms.CharField(label=u'Arrestado', required=True)
    arrested = forms.CharField(widget=forms.HiddenInput, required=True)
    formfield_callback = make_custom_datefield_for_arrest
    
    class Meta:
        model = Arrest
        exclude = ('approved_by_ops', 'arrested')
        fields = ('date', 'arrested_select', 'time', 'was_notified', 'description')
        
class ArrestPaymentForm(forms.Form):
    formfield_callback = make_custom_datefield_for_arrest
    
    payer_select = forms.CharField(label=u'Persona que paga arresto', required=True)
    payer = forms.CharField(widget=forms.HiddenInput, required=True)
    start_time_date = forms.DateField(label=u"Fecha de Inicio")
    start_time_time = forms.TimeField(label=u"Hora de Inicio", help_text=u"HHMM")
    end_time_date = forms.DateField(label=u"Fecha de Fin")
    end_time_time = forms.TimeField(label=u"Hora de Fin", help_text=u"HHMM")
    