# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ArrestPayment'
        db.create_table(u'ops_arrestpayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='arrest_payments_created', null=True, to=orm['personal.Firefighter'])),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='arrests_payments', null=True, to=orm['personal.Firefighter'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('minutes', self.gf('django.db.models.fields.IntegerField')()),
            ('approved_by_ops', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'ops', ['ArrestPayment'])

        # Adding model 'Arrest'
        db.create_table(u'ops_arrest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='arrests_created', null=True, to=orm['personal.Firefighter'])),
            ('arrested', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='arrests', null=True, to=orm['personal.Firefighter'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('was_notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time', self.gf('django.db.models.fields.IntegerField')()),
            ('minutes', self.gf('django.db.models.fields.IntegerField')()),
            ('approved_by_ops', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'ops', ['Arrest'])


    def backwards(self, orm):
        
        # Deleting model 'ArrestPayment'
        db.delete_table(u'ops_arrestpayment')

        # Deleting model 'Arrest'
        db.delete_table(u'ops_arrest')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 30, 0, 41, 51, 636071)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 30, 0, 41, 51, 635562)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.City']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'map_location': ('common.widgets.LocationField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'common.baseperson': {
            'Meta': {'object_name': 'BasePerson'},
            'alternate_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_document': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_name_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'primary_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'})
        },
        u'common.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'common.company': {
            'Meta': {'object_name': 'Company'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Address']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rif': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'common.course': {
            'Meta': {'object_name': 'Course'},
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.School']"})
        },
        u'common.degree': {
            'Meta': {'object_name': 'Degree'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.School']"})
        },
        u'common.job': {
            'Meta': {'object_name': 'Job'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'common.person': {
            'Meta': {'object_name': 'Person', '_ormbases': [u'common.BasePerson']},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Address']", 'null': 'True', 'through': u"orm['common.PersonAddress']", 'symmetrical': 'False'}),
            u'baseperson_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.BasePerson']", 'unique': 'True', 'primary_key': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_place': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'born_here'", 'unique': 'True', 'null': 'True', 'to': u"orm['common.Address']"}),
            'childs': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['common.BasePerson']"}),
            'civil_state': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Course']", 'null': 'True', 'through': u"orm['common.PersonCourse']", 'symmetrical': 'False'}),
            'degrees': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Degree']", 'null': 'True', 'through': u"orm['common.PersonDegree']", 'symmetrical': 'False'}),
            'jobs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Job']", 'null': 'True', 'through': u"orm['common.PersonJob']", 'symmetrical': 'False'}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'common.personaddress': {
            'Meta': {'object_name': 'PersonAddress'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Address']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Person']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'common.personcourse': {
            'Meta': {'object_name': 'PersonCourse'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Person']"}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'training_course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Course']"})
        },
        u'common.persondegree': {
            'Meta': {'object_name': 'PersonDegree'},
            'degree': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Degree']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Person']"}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'common.personjob': {
            'Meta': {'object_name': 'PersonJob'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Job']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Person']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'supervised_set'", 'null': 'True', 'to': u"orm['common.BasePerson']"})
        },
        u'common.school': {
            'Meta': {'object_name': 'School'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ops.arrest': {
            'Meta': {'object_name': 'Arrest'},
            'approved_by_ops': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'arrested': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'arrests'", 'null': 'True', 'to': u"orm['personal.Firefighter']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'arrests_created'", 'null': 'True', 'to': u"orm['personal.Firefighter']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.IntegerField', [], {}),
            'was_notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'ops.arrestpayment': {
            'Meta': {'object_name': 'ArrestPayment'},
            'approved_by_ops': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'arrest_payments_created'", 'null': 'True', 'to': u"orm['personal.Firefighter']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.IntegerField', [], {}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'arrests_payments'", 'null': 'True', 'to': u"orm['personal.Firefighter']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'ops.service': {
            'Meta': {'ordering': "['-id', 'date']", 'object_name': 'Service'},
            'affected': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['ops.ServiceAffected']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'services_created'", 'null': 'True', 'to': u"orm['personal.Firefighter']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'map_location': ('common.widgets.LocationField', [], {'max_length': '255', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'time': ('django.db.models.fields.TimeField', [], {})
        },
        u'ops.serviceaffected': {
            'Meta': {'object_name': 'ServiceAffected'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'person_affected': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services_involved'", 'to': u"orm['common.BasePerson']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        u'ops.servicevehicle': {
            'Meta': {'object_name': 'ServiceVehicle'},
            'crew': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'in_services'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['personal.Firefighter']"}),
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'services_drove'", 'null': 'True', 'to': u"orm['personal.Firefighter']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services_lead'", 'to': u"orm['personal.Firefighter']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vehicles'", 'to': u"orm['ops.Service']"}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ops.Vehicle']", 'null': 'True', 'blank': 'True'})
        },
        u'ops.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'personal.firefighter': {
            'Meta': {'ordering': "['-number', 'last_name']", 'object_name': 'Firefighter', '_ormbases': [u'common.Person']},
            'blood_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'blood_type_rh': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'profile_picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ranks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['personal.Rank']", 'null': 'True', 'through': u"orm['personal.RankChange']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'personal.rank': {
            'Meta': {'object_name': 'Rank'},
            'abrev': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'personal.rankchange': {
            'Meta': {'object_name': 'RankChange'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'firefighter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['personal.Firefighter']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank_obtained': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['personal.Rank']"})
        }
    }

    complete_apps = ['ops']
