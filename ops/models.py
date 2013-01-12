#coding=utf-8
from django.db import models
from common.widgets import LocationField
from personal.models import Firefighter
from common.models import BasePerson


class Vehicle(models.Model):
    class Meta:
        verbose_name = "Vehiculo"
        verbose_name_plural = "Vehiculos"

    name = models.CharField(max_length=100, verbose_name="Nombre de Unidad")
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class ServiceAffected(models.Model):
    class Meta:
        verbose_name = "Afectado"
        verbose_name_plural = "Afectados"

    AFFECTED_TYPE_CHOICES = (
                            (u'EST', u'Estudiante de la USB'),
                            (u'PROF', u'Profesor de la USB'),
                            (u'EMP', u'Empleado de la USB'),
                            (u'OBR', u'Obrero de la USB'),
                            (u'NA', u'Externo'),
                            )

    person_affected = models.ForeignKey(BasePerson, related_name="services_involved")
    notes = models.TextField(verbose_name=u"Notas/Tratamiento")
    type = models.CharField(max_length=6, choices=AFFECTED_TYPE_CHOICES, verbose_name="Tipo")

    def __unicode__(self):
        return str(self.person_affected)


class Service(models.Model):
    class Meta:
        ordering = ['-id', 'date']
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    SERVICE_TYPE_CHOICES = (
                            (u'CM', u'Control Médico'),
                            (u'AME1', u'Atención Médica de Emergencia'),
                            (u'AME2', u'Atención Médica de Enfermo'),
                            (u'IDE', u'Incendio de Estructura'),
                            (u'IDV', u'Incendio de Vegetación'),
                            (u'PC', u'Prevención y Control'),
                            (u'AY', u'Apoyo a la comunidad'),
                            (u'MP', u'Matpel'),
                            (u'RES1', u'Rescate de Personas'),
                            (u'RES2', u'Rescate Animal'),
                            (u'SE', u'Servicio Especial'),
                            (u'GP', u'Guardia de Prevención'),
                            (u'NSA', u'No se actuó'),
                            (u'FA', u'Falsa Alarma'),
                            )

    creation_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Firefighter, related_name='services_created', editable=False, null=True, blank=True)

    date = models.DateField(verbose_name="Fecha")
    time = models.TimeField(verbose_name="Hora", help_text=u"HHMM")

    service_type = models.CharField(max_length=6, choices=SERVICE_TYPE_CHOICES, verbose_name="Tipo")
    description = models.TextField(verbose_name=u"Descripción")

    affected = models.ManyToManyField(ServiceAffected, verbose_name=u"Afectados")

    location = models.TextField(verbose_name=u'Dirección', null=True, blank=True)
    map_location = LocationField(verbose_name=u'Ubicación en Mapa', blank=True, max_length=255)


class ServiceVehicle(models.Model):
    class Meta:
        verbose_name = "Unidad en Servicio"
        verbose_name_plural = "Unidades en Servicio"

    service = models.ForeignKey(Service, related_name='vehicles', verbose_name=u"Servicio")
    lead = models.ForeignKey(Firefighter, related_name='services_lead', verbose_name=u"Jefe de Servicio")
    crew = models.ManyToManyField(Firefighter, related_name="in_services", verbose_name=u"Tripulación", null=True, blank=True)
    driver = models.ForeignKey(Firefighter, related_name="services_drove", verbose_name=u"Conductor", null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, verbose_name=u"Unidad", null=True, blank=True)
