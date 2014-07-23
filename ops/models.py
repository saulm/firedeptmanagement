#coding=utf-8
from django.db import models
from common.widgets import LocationField
from personal.models import Firefighter
from common.models import BasePerson
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import logging
from sorl.thumbnail import ImageField
from datetime import datetime

logger = logging.getLogger('django')

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

    date = models.DateField(verbose_name="Fecha de inicio")
    time = models.TimeField(verbose_name="Hora de inicio", help_text=u"HHMM")
    
    scene_arrival_date = models.DateField(verbose_name="Fecha de llegada al sitio", null=True)
    scene_arrival_time = models.TimeField(verbose_name="Hora de llegada al sitio", help_text=u"HHMM", null=True)
    
    end_date = models.DateField(verbose_name=u"Fecha de regreso a la estación (Fin del Servicio)", null=True)
    end_time = models.TimeField(verbose_name=u"Hora de regreso a la estación (Fin del Servicio)", help_text=u"HHMM", null=True)
    
    service_type = models.CharField(max_length=6, choices=SERVICE_TYPE_CHOICES, verbose_name="Tipo")
    description = models.TextField(verbose_name=u"Descripción")
    
    affected = models.ManyToManyField(ServiceAffected, verbose_name=u"Afectados", null=True, blank=True)

    location = models.TextField(verbose_name=u'Dirección', null=True, blank=True)
    map_location = LocationField(verbose_name=u'Ubicación en Mapa', blank=True, max_length=255)
    
    def start_as_dt(self):
        if self.date and self.time:
            return datetime.combine(self.date, self.time)
        return None
    
    def arrival_as_dt(self):
        if self.scene_arrival_date and self.scene_arrival_time:
            return datetime.combine(self.scene_arrival_date, self.scene_arrival_time)
        return None
    
    def end_as_dt(self):
        if self.end_date and self.end_time:
            return datetime.combine(self.end_date, self.end_time)
        return None
    
    def response_time(self):
        try:
            return self.arrival_as_dt() - self.start_as_dt()
        except:
            return None 
    
    def duration(self):
        try:
            return self.end_as_dt() - self.start_as_dt()
        except:
            return None 
    
    def clean(self):
        start = self.start_as_dt()
        scene_arrival = self.arrival_as_dt()
        end = self.end_as_dt()
        if not start or not scene_arrival or not end:
            raise ValidationError(u"Asegurate de insertar todas las fechas/horas")
        if not scene_arrival >= start:
            raise ValidationError(u"La fecha de llegada al sitio tiene que ser mayor o igual que la fecha de inicio")
        if not end > scene_arrival:
            raise ValidationError(u"La fecha de fin del servicio tiene que ser mayor que la fecha de llegada al sitio")
        
    def complete_crew(self):
        complete_crew = set()
        for vehicle in self.vehicles.all():
            complete_crew.update(vehicle.complete_crew())
        return list(complete_crew)

class ServiceVehicle(models.Model):
    class Meta:
        verbose_name = "Unidad en Servicio"
        verbose_name_plural = "Unidades en Servicio"

    service = models.ForeignKey(Service, related_name='vehicles', verbose_name=u"Servicio")
    lead = models.ForeignKey(Firefighter, related_name='services_lead', verbose_name=u"Jefe de Servicio")
    crew = models.ManyToManyField(Firefighter, related_name="in_services", verbose_name=u"Tripulación", null=True, blank=True)
    driver = models.ForeignKey(Firefighter, related_name="services_drove", verbose_name=u"Conductor", null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, verbose_name=u"Unidad", null=True, blank=True)
    
    def complete_crew(self):
        complete_crew = set(self.crew.all())
        complete_crew.add(self.lead)
        if self.driver != None:
            complete_crew.add(self.driver)
        return list(complete_crew)
    
class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name='images', verbose_name=u"Servicio")
    uploader = models.ForeignKey(Firefighter)
    file = ImageField(upload_to="images/services/", verbose_name='Foto')
    
class Arrest(models.Model):
    class Meta:
        verbose_name = u"Arresto"
        verbose_name_plural = u"Arrestos"

    creation_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Firefighter, related_name='arrests_created', editable=False, null=True, blank=True, verbose_name='Agregado por')
    arrested = models.ForeignKey(Firefighter, related_name="arrests", verbose_name=u"Arrestado", null=True, blank=True)
    date = models.DateField(verbose_name=u"Fecha")
    description = models.TextField(verbose_name=u"Descripción")
    was_notified = models.BooleanField(default=False, verbose_name=u"Notificó")
    time = models.IntegerField(verbose_name=u'Minutos de ausencia', validators=[MinValueValidator(0)])
    minutes = models.IntegerField(verbose_name=u'Minutos de arresto', editable=False, validators=[MinValueValidator(0)])
    approved_by_ops = models.BooleanField(default=True, verbose_name=u"Aprobado por Operaciones")
    approved_by_inspector = models.BooleanField(default=True, verbose_name=u"Aprobado por el Inspector")

    def save(self, *args, **kwargs):
        self.minutes = self.time*1.5 if self.was_notified else self.time*2
        super(Arrest, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return u"%s %s %s" % (unicode(self.date), unicode(self.minutes), unicode(self.arrested))

@receiver(post_save, sender=Arrest)
def notify_arrested(sender, instance, created, **kwargs):
    logger.info("Sending Arrest Email")
    if created:
        subject = u"Nuevo Arresto"
        content = u"%s te ha insertado un nuevo arresto:\n\n%s\n\n%s, este debe ser aprobado por operaciones  e Inspectoria para ser actualizado en tus arrestos" % (unicode(instance.created_by), unicode(instance), unicode(instance.description))
        send_mail(subject, content, settings.DEFAULT_FROM_EMAIL, [instance.arrested.primary_email,], fail_silently=True)
    else:
        subject = u"Actualización Arrestos"
        content = u"Tus arrestos han sido actualizados, chequea tu perfil para más información"
        send_mail(subject, content, settings.DEFAULT_FROM_EMAIL, [instance.arrested.primary_email,], fail_silently=True)

class ArrestPayment(models.Model):
    class Meta:
        verbose_name = u"Pago de Arresto"
        verbose_name_plural = u"Pagos de Arresto"

    creation_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Firefighter, related_name=u'arrest_payments_created', editable=False, null=True, blank=True, verbose_name='Agregado por')
    payer = models.ForeignKey(Firefighter, related_name=u"arrests_payments", verbose_name=u"Persona que paga el arresto", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name=u"Fecha/Hora de inicio")
    end_time = models.DateTimeField(verbose_name=u"Fecha/Hora de fin")
    minutes = models.IntegerField(verbose_name=u'Minutos', validators=[MinValueValidator(0)], editable=False)
    approved_by_ops = models.BooleanField(default=False, verbose_name=u"Aprobado por Operaciones")
    
    def save(self, *args, **kwargs):
        delta = self.end_time - self.start_time
        self.minutes = int( delta.total_seconds()/60 )
        super(ArrestPayment, self).save(*args, **kwargs)
    
    def clean(self):
        delta = self.end_time - self.start_time
        mins  = int( delta.total_seconds()/60 )
        
        if self.end_time <= self.start_time:
            raise ValidationError(u'La fecha de fin debe ser mayor que la fecha de inicio')
        if mins > self.payer.total_arrests():
            raise ValidationError(u'No puedes pagar más arrestos de los que debes, actualmente debes %d minutos, estas tratando de insertar %d' % (self.payer.total_arrests(), mins))
    
    def __unicode__(self):
        return u"%s %s %s" % (unicode(self.start_time),  unicode(self.minutes), unicode(self.payer))

@receiver(post_save, sender=ArrestPayment)
def notify_arrest_payment(sender, instance, created, **kwargs):
    logger.info("Sending Arrest Payment Email")
    if created:
        subject = u"Nuevo Pago Arresto"
        content = u"%s te ha insertado un nuevo pago de arresto:\n\n%s\n\nEste debe ser aprobado por operaciones para ser actualizado en tus arrestos" % (unicode(instance.created_by), unicode(instance))
        send_mail(subject, content, settings.DEFAULT_FROM_EMAIL, [instance.payer.primary_email,], fail_silently=True)
    else:
        subject = u"Actualización Pago de Arresto"
        content = u"Tus pagos de arresto han sido actualizados, chequea tu perfil para más información"
        send_mail(subject, content, settings.DEFAULT_FROM_EMAIL, [instance.payer.primary_email,], fail_silently=True)
    
