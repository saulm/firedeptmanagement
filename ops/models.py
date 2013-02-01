#coding=utf-8
from django.db import models
from common.widgets import LocationField
from personal.models import Firefighter
from common.models import BasePerson
from django.core.validators import MinValueValidator

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
        ordering = ['-date', '-time']
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
    
    affected = models.ManyToManyField(ServiceAffected, verbose_name=u"Afectados", null=True, blank=True)

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


class Arrest(models.Model):
    class Meta:
        verbose_name = "Arresto"
        verbose_name_plural = "Arrestos"

    creation_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Firefighter, related_name='arrests_created', editable=False, null=True, blank=True)
    arrested = models.ForeignKey(Firefighter, related_name="arrests", verbose_name=u"Arrestado", null=True, blank=True)
    date = models.DateField(verbose_name="Fecha")
    description = models.TextField(verbose_name=u"Descripción")
    was_notified = models.BooleanField(default=False, verbose_name=u"Notificó")
    time = models.IntegerField(verbose_name=u'Minutos de ausencia', validators=[MinValueValidator(0)])
    minutes = models.IntegerField(verbose_name=u'Minutos de arresto', editable=False, validators=[MinValueValidator(0)])
    approved_by_ops = models.BooleanField(default=False, verbose_name=u"Aprobado por Operaciones")
    
    def save(self, *args, **kwargs):
        self.minutes = self.time if self.was_notified else self.time*1.5
        super(Arrest, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return "%s %s %s" % (str(self.date), str(self.minutes), str(self.arrested))

class ArrestPayment(models.Model):
    class Meta:
        verbose_name = "Pago de Arresto"
        verbose_name_plural = "Pagos de Arresto"

    creation_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Firefighter, related_name='arrest_payments_created', editable=False, null=True, blank=True)
    payer = models.ForeignKey(Firefighter, related_name="arrests_payments", verbose_name=u"Arrestado", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="Fecha de inicio")
    end_time = models.DateTimeField(verbose_name="Fecha de fin")
    minutes = models.IntegerField(verbose_name=u'Minutos', validators=[MinValueValidator(0)], editable=False)
    approved_by_ops = models.BooleanField(default=False, verbose_name=u"Aprobado por Operaciones")
    
    def save(self, *args, **kwargs):
        delta = self.end_time - self.start_time
        self.minutes = int(delta.total_seconds()/60)
        super(ArrestPayment, self).save(*args, **kwargs)
    