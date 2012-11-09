# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class ActiveSessions(models.Model):
    sid = models.CharField(max_length=96, primary_key=True)
    name = models.CharField(max_length=96, primary_key=True)
    val = models.TextField(blank=True)
    changed = models.CharField(max_length=42)
    class Meta:
        db_table = u'active_sessions'

class Anuncios(models.Model):
    aid = models.IntegerField(primary_key=True)
    fecha = models.DateTimeField()
    autor = models.CharField(max_length=48)
    titulo = models.CharField(max_length=765)
    texto = models.TextField(blank=True)
    class Meta:
        db_table = u'anuncios'

class Arresto(models.Model):
    persona = models.CharField(max_length=48)
    exp = models.IntegerField(null=True, blank=True)
    factor = models.FloatField()
    minutos = models.FloatField()
    fecha = models.DateField()
    fecha_ins = models.DateTimeField(primary_key=True)
    ins_por = models.CharField(max_length=48)
    class Meta:
        db_table = u'arrestos'

    def __unicode__(self):
        return "%s %s %d" % (str(self.fecha), self.persona, self.minutos)

#class AuthUser(models.Model):
    # uid = models.CharField(max_length=96, primary_key=True)
    # username = models.CharField(unique=True, max_length=96)
    # password = models.CharField(max_length=96)
    # perms = models.CharField(max_length=765, blank=True)
    # class Meta:
    #     db_table = u'auth_user'

class Avances(models.Model):
    id_proy = models.IntegerField(primary_key=True)
    fecha = models.DateTimeField(primary_key=True)
    porcentaje = models.IntegerField()
    class Meta:
        db_table = u'avances'

class EvalOperativa(models.Model):
    ci = models.IntegerField(primary_key=True, db_column='CI') # Field name made lowercase.
    fecha_guardia = models.DateField(primary_key=True)
    evaluador = models.IntegerField(primary_key=True)
    fecha_eval = models.DateTimeField()
    jefe = models.CharField(max_length=9)
    estado = models.CharField(max_length=51)
    item1 = models.IntegerField(null=True, blank=True)
    item2 = models.IntegerField(null=True, blank=True)
    item3 = models.IntegerField(null=True, blank=True)
    item4 = models.IntegerField(null=True, blank=True)
    item5 = models.IntegerField(null=True, blank=True)
    item6 = models.IntegerField(null=True, blank=True)
    item7 = models.IntegerField(null=True, blank=True)
    item8 = models.IntegerField(null=True, blank=True)
    item9 = models.IntegerField(null=True, blank=True)
    item10 = models.IntegerField(null=True, blank=True)
    item11 = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eval_operativa'

class Expediente(models.Model):
    exp = models.IntegerField(primary_key=True)
    ult_mod = models.DateTimeField()
    persona = models.CharField(max_length=48)
    encargado = models.CharField(max_length=48, blank=True)
    fecha = models.DateField()
    apertura = models.DateTimeField()
    finalizado = models.DateTimeField()
    apelado = models.IntegerField()
    sancion = models.CharField(max_length=195, blank=True)
    class Meta:
        db_table = u'expedientes'

    def __unicode__(self):
        return "%d %s %s %s" % (self.exp, self.persona, self.fecha, self.sancion)


class Expulsiones(models.Model):
    persona = models.CharField(max_length=48)
    exp = models.IntegerField()
    tiempo = models.CharField(max_length=9)
    fecha_ins = models.DateTimeField()
    por = models.CharField(max_length=48)
    class Meta:
        db_table = u'expulsiones'

class Hh(models.Model):
    id_hh = models.IntegerField(unique=True)
    persona = models.CharField(max_length=48)
    minutos = models.IntegerField()
    id_proy = models.IntegerField(null=True, blank=True)
    fecha = models.DateField()
    fecha_ins = models.DateTimeField()
    descripcion = models.TextField()
    certificador = models.CharField(max_length=48, blank=True)
    status = models.CharField(max_length=33)
    class Meta:
        db_table = u'hh'

class Jefes(models.Model):
    login = models.CharField(max_length=96)
    grupo = models.CharField(max_length=42)
    class Meta:
        db_table = u'jefes'

class Metas(models.Model):
    id_meta = models.IntegerField(primary_key=True)
    meta = models.CharField(max_length=765)
    id_proy = models.IntegerField()
    finalizada = models.CharField(max_length=9)
    class Meta:
        db_table = u'metas'

class ObsExpedientes(models.Model):
    exp = models.ForeignKey(Expediente, db_column='exp')
    fecha = models.DateTimeField(primary_key=True)
    obs = models.TextField()
    por = models.CharField(max_length=48)
    class Meta:
        db_table = u'obs_expedientes'

    def __unicode__(self):
        return "%s %s" % (self.fecha, self.obs)


class Personal(models.Model):
    ape = models.CharField(max_length=75)
    nom = models.CharField(max_length=75)
    login = models.CharField(unique=True, max_length=48)
    grupo = models.CharField(max_length=42, blank=True)
    ci = models.IntegerField(primary_key=True, db_column='CI') # Field name made lowercase.
    car = models.IntegerField(null=True, blank=True)
    carnet = models.IntegerField(null=True, blank=True)
    jer = models.CharField(max_length=18)
    ape2 = models.CharField(max_length=45, blank=True)
    nom2 = models.CharField(max_length=45, blank=True)
    sex = models.CharField(max_length=3)
    fn = models.DateField(null=True, blank=True)
    sangre = models.CharField(max_length=6, blank=True)
    rh = models.CharField(max_length=3, blank=True)
    ult_mod = models.DateTimeField()
    mod_por = models.CharField(max_length=45, blank=True)
    cargo = models.CharField(max_length=180, blank=True)
    tel = models.CharField(max_length=33, blank=True)
    tel2 = models.CharField(max_length=33, blank=True)
    cel = models.CharField(max_length=33, blank=True)
    ult_asc = models.DateField(null=True, blank=True)
    condicion = models.CharField(max_length=9)
    class Meta:
        db_table = u'personal'

class Proyectos(models.Model):
    id_proy = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=765)
    descripcion = models.TextField(blank=True)
    encargado = models.CharField(max_length=765)
    grupo = models.CharField(max_length=48, blank=True)
    prioridad = models.CharField(max_length=72)
    finalizado = models.CharField(max_length=9)
    fec_ini = models.DateField()
    fec_est = models.DateField()
    fec_fin = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'proyectos'

class Servicio(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    fecha = models.DateField(unique=True)
    hora = models.TextField(unique=True) # This field type is a guess.
    tipo = models.CharField(max_length=9)
    fansa = models.CharField(max_length=9, blank=True)
    enusb = models.CharField(max_length=6, blank=True)
    miemusb = models.CharField(max_length=9, blank=True)
    grupo = models.CharField(max_length=9)
    unidad = models.CharField(max_length=9, blank=True)
    nro_per = models.IntegerField(null=True, blank=True)
    jc = models.CharField(max_length=45)
    c = models.CharField(max_length=45, blank=True)
    ac = models.CharField(max_length=765, blank=True)
    ingresado = models.DateTimeField()
    por = models.CharField(max_length=96)
    descripcion = models.TextField(blank=True)
    class Meta:
        db_table = u'servicios2'

    def __unicode__(self):
        return "%s %s %s" % (str(self.fecha), self.tipo, self.jc)


class Suspensiones(models.Model):
    persona = models.CharField(max_length=48)
    exp = models.IntegerField(unique=True)
    semanas = models.IntegerField()
    fecha_ins = models.DateTimeField()
    por = models.CharField(max_length=48)
    class Meta:
        db_table = u'suspensiones'

