#coding=utf-8
from django.db import models
from firedeptmanagement.common.models import BasePerson, Company
from firedeptmanagement.personal.models import Firefighter
from django.db.models import Q

CONTACT_TYPE_CHOICES = (
                         (u'C', u'Cliente'),
                         (u'O', u'Contacto'),
                         (u'A', u'Ambos'),
                        )
    
class RelationalPerson(BasePerson):
    class Meta:
        verbose_name = u"Persona"
    observation = models.TextField(verbose_name = u'Observación', null=True, blank=True)
    type=models.CharField(verbose_name = u'Tipo', max_length=1, choices=CONTACT_TYPE_CHOICES, null=True, blank=True)
         
class RelationalCompany(Company):
    class Meta:
        verbose_name = u"Empresa"
 
    COMPANY_TYPE_CHOICES = (
                         (u'T', u'Cuerpo de Bomberos'),
                         (u'H', u'Hospitales'),
                         (u'R', u'Grupos de Rescate'),
                         (u'P', u'Empresa Privada'),
                         (u'U', u'Dependencia USB'),
                         (u'G', u'Empresa Pública'),
                         (u'C', u'Agrupación Civil'),
                         (u'O', u'Otro'),
                         )
    
    person = models.ManyToManyField(RelationalPerson, through='Position')
    typecompany = models.CharField(verbose_name = u'Tipo de Empresa', max_length=1, choices=COMPANY_TYPE_CHOICES)
    observation = models.TextField(verbose_name = u'Observación', null=True, blank=True)
    type=models.CharField(verbose_name = u'Tipo', max_length=1, choices=CONTACT_TYPE_CHOICES, null=True, blank=True)
    
    @classmethod
    def search(cls, text):
        return cls.objects.filter(
                           Q(name__icontains=text) | 
                           Q(address__city__name__icontains=text) |
                           Q(address__location__icontains=text) |
                           Q(rif__icontains=text) |
                           Q(website__icontains=text) |
                           Q(email__icontains=text) |
                           Q(observation__icontains=text) 
        ).order_by("name")
    
    
class Position(models.Model):
    class Meta:
        verbose_name = u"Cargo"
    
    person = models.ForeignKey(RelationalPerson, verbose_name=u"Persona")
    company = models.ForeignKey(RelationalCompany, verbose_name=u"Compania")
    position = models.CharField(max_length = 100,verbose_name = u'Posición en la Empresa')
    observation = models.TextField(verbose_name = u'Observación', null=True, blank=True)
     
class Relationship(models.Model):
    class Meta:
        verbose_name = u"Relación"
        verbose_name_plural = u'Relaciones'
 
    relational_person = models.ForeignKey(RelationalPerson,  verbose_name = u'Persona Relacionada', null=True, blank=True)
    firefighter = models.ForeignKey(Firefighter,  verbose_name = u'Bombero Relacionado', null=True, blank=True )
    observation = models.TextField(verbose_name = u'Observación', null=True, blank=True)
