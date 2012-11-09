#coding=utf-8
from django.db import models
from common.widgets import LocationField
from django.forms import ModelForm
from sorl.thumbnail import ImageField

class TelephoneNumber(models.Model):
    class Meta:
        verbose_name = u"Número Telefónico"
        verbose_name_plural = u'Números Telefónicos'

    code = models.CharField(max_length=4, verbose_name=u'Código')
    number = models.CharField(max_length=7, verbose_name=u'Número')

    def __unicode__(self):
        return "%s-%s" % (self.code, self.number)

class City(models.Model):
    class Meta:
        verbose_name = u"Ciudad"
        verbose_name_plural = u'Ciudades'

    name = models.CharField(max_length=250, verbose_name=u'Nombre')

    def __unicode__(self):
        return self.name

class Address(models.Model):
    class Meta:
        verbose_name = u"Dirección"
        verbose_name_plural = u'Direcciones'

    city = models.ForeignKey(City, verbose_name=u'Ciudad', null=True, blank=True)
    location = models.TextField(verbose_name=u'Detalle', null=True, blank=True)
    map_location = LocationField(verbose_name=u'Ubicación en Mapa', blank=True, max_length=255)

    def __unicode__(self):
        return self.location

class School(models.Model):
    class Meta:
        verbose_name = u"Institución Educativa"
        verbose_name_plural = u'Instituciones Educativas'


    name = models.CharField(verbose_name=u'Nombre', max_length=100)

    def __unicode__(self):
        return self.name

class Degree(models.Model):
    class Meta:
        verbose_name = u"Estudio"

    DEGREE_LEVEL_CHOICES = (
                            (u'TSU', u'Técnico Superior Universitario'),
                            (u'PREG', u'Pregrado (Licenciatura/Ingeniería)'),
                            (u'DIP', u'Diplomado'),
                            (u'ESP', u'Especialización'),
                            (u'MAES', u'Maestría'),
                            (u'DOCT', u'Doctorado'),
                            (u'PDOC', u'Postdoctorado'),
                            )

    name = models.CharField(verbose_name=u'Nombre', max_length=100)
    level = models.CharField(verbose_name=u'Tipo', max_length=4, choices=DEGREE_LEVEL_CHOICES)
    school = models.ForeignKey(School, verbose_name=u'Institución')

    def __unicode__(self):
        return "%s %s - %s" % (self.level, self.name, self.school.name)

class Course(models.Model):
    class Meta:
        verbose_name = u"Curso"

    name = models.CharField(verbose_name=u'Nombre', max_length=100)
    school = models.ForeignKey(School, verbose_name=u'Institución')
    hours = models.IntegerField()

    def __unicode__(self):
        return "%s (%d h) - %s" % (self.name, self.hours, self.school.name)

class Company(models.Model):
    class Meta:
        verbose_name = u"Compañia"

    name = models.CharField(verbose_name=u'Nombre', max_length=100)
    address = models.ForeignKey(Address, null=True, blank=True, verbose_name='Dirección')
    rif = models.CharField(verbose_name=u'RIF', null=True, blank=True, max_length=10)
    website = models.CharField(verbose_name=u'Página Web', null=True, blank=True, max_length=50)
    email = models.EmailField(null=True, blank=True, verbose_name=u'Email')

    def __unicode__(self):
        return self.name

class Job(models.Model):
    class Meta:
        verbose_name = u"Trabajo"

    company = models.ForeignKey(Company)
    title = models.CharField(u'Cargo', max_length=100)

    def __unicode__(self):
        return "%s - %s" % (self.title, self.company.name)

class BasePerson(models.Model):
    class Meta:
        verbose_name = u"Persona Min"

    GENDER_CHOICES = (
        (u'M', u'Masculino'),
        (u'F', u'Femenino'),
    )

    first_name = models.CharField(verbose_name=u'Primer Nombre', max_length=100)
    first_name_2 = models.CharField(verbose_name=u'Segundo Nombre', max_length=100, null=True, blank=True)
    last_name = models.CharField(verbose_name=u'Primer Apellido', max_length=100)
    last_name_2 = models.CharField(verbose_name=u'Segundo Apellido', max_length=100, null=True, blank=True)
    id_document = models.CharField(verbose_name=u'Cédula', max_length=10, null=True, blank=True)
    gender = models.CharField(verbose_name=u'Sexo', max_length=2, choices=GENDER_CHOICES, null=True, blank=True)
    primary_email = models.EmailField(null=True, blank=True, verbose_name='Email Principal')
    alternate_email = models.EmailField(null=True, blank=True, verbose_name='Email Alterno')

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

class PersonTelephoneNumber(models.Model):
    class Meta:
        verbose_name = u"Número Telefónico"
        verbose_name_plural = u'Números Telefónicos'

    TELEPHONE_TYPE_CHOICES = (
                         (u'T', u'Trabajo'),
                         (u'C', u'Casa'),
                         (u'M', u'Celular'),
                         (u'O', u'Otro'),
                         )

    person = models.ForeignKey(BasePerson)
    type = models.CharField(verbose_name=u'Tipo', max_length=1, choices=TELEPHONE_TYPE_CHOICES, default='O')
    telephone_number = models.ForeignKey(TelephoneNumber)
    main = models.BooleanField(verbose_name='Principal', default=True)

    def __unicode__(self):
        return self.get_type_display() + ": " + str(self.telephone_number)

class CompanyTelephoneNumber(models.Model):
    class Meta:
        verbose_name = u"Número Telefónico"
        verbose_name_plural = u'Números Telefónicos'

    company = models.ForeignKey(Company)
    telephone_number = models.ForeignKey(TelephoneNumber)
    main = models.BooleanField(verbose_name='Principal', default=True)

    def __unicode__(self):
        return str(self.telephone_number)


class Person(BasePerson):
    class Meta:
        verbose_name = u"Persona"


    CIVIL_STATE_CHOICES = (
        (u'S', u'Soltero'),
        (u'C', u'Casado'),
        (u'V', u'Viudo'),
        (u'D', u'Divorciado'),

    )

    birth_date = models.DateField(verbose_name=u'Fecha de Nacimiento', null=True, blank=True)
    birth_place = models.OneToOneField(Address, related_name='born_here', verbose_name='Lugar de Nacimiento', null=True, blank=True)
    picture = ImageField(upload_to="images/persons/", null=True, blank=True, verbose_name='Foto')
    addresses = models.ManyToManyField(Address, verbose_name=u'Direcciones', through="PersonAddress", null=True)
    degrees = models.ManyToManyField(Degree, through="PersonDegree", null=True, verbose_name=u'Estudios')
    courses = models.ManyToManyField(Course, through="PersonCourse", null=True, verbose_name=u'Cursos')
    jobs = models.ManyToManyField(Job, through="PersonJob", null=True, verbose_name=u'Trabajos')
    childs = models.ManyToManyField(BasePerson, null=True, blank=True, verbose_name=u'Hijos', related_name="child_set")
    civil_state = models.CharField(verbose_name=u'Estado Civil', max_length=1, choices=CIVIL_STATE_CHOICES, null=True, blank=True)

class PersonAddress(models.Model):
    class Meta:
        verbose_name = u"Dirección"
        verbose_name_plural = u"Direcciones"


    ADDRESS_TYPE_CHOICES = (
                            (u'C', u'Casa'),
                            (u'T', u'Trabajo'),
                            (u'O', u'Otro'),
                            )

    type = models.CharField(verbose_name=u'Tipo', max_length=1, choices=ADDRESS_TYPE_CHOICES)
    person = models.ForeignKey(Person, verbose_name=u'Persona')
    address = models.ForeignKey(Address, verbose_name=u'Dirección')

class PersonDegree(models.Model):
    class Meta:
        verbose_name = u"Estudio"

    person = models.ForeignKey(Person, verbose_name=u'Persona')
    degree = models.ForeignKey(Degree, verbose_name=u'Estudio')
    start_date = models.DateField(verbose_name=u'Fecha de Inicio')
    end_date = models.DateField(verbose_name=u'Fecha de Finalización', null=True, blank=True)
    picture = models.ImageField(upload_to="images/degrees/", null=True, blank=True, verbose_name=u'Imagen Título')

class PersonCourse(models.Model):
    class Meta:
        verbose_name = u"Curso"

    person = models.ForeignKey(Person, verbose_name=u'Persona')
    training_course = models.ForeignKey(Course, verbose_name=u'Curso')
    date = models.DateField(verbose_name=u'Fecha de Realización')
    picture = models.ImageField(upload_to="images/courses/", null=True, blank=True, verbose_name=u'Imagen Certificado')

class PersonJob(models.Model):
    class Meta:
        verbose_name = u"Trabajo"

    person = models.ForeignKey(Person, verbose_name=u'Persona')
    job = models.ForeignKey(Job, verbose_name=u'Trabajo')
    start_date = models.DateField(verbose_name=u'Fecha de Inicio')
    end_date = models.DateField(verbose_name=u'Fecha de Finalización', null=True, blank=True)
    supervisor = models.ForeignKey(BasePerson, null=True, blank=True, related_name='supervised_set', verbose_name='Supervisor')


class Suggestion(models.Model):
    date = models.DateTimeField(auto_now=True, verbose_name=u'Fecha')
    text = models.TextField(verbose_name=u'Sugerencia')

class SuggestionForm(ModelForm):
    class Meta:
        model = Suggestion
