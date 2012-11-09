# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'ServiceAffected'
        db.create_table('ops_serviceaffected', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person_affected', self.gf('django.db.models.fields.related.ForeignKey')(related_name='services_involved', to=orm['common.BasePerson'])),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('ops', ['ServiceAffected'])

        # Removing M2M table for field patients on 'Service'
        db.delete_table('ops_service_patients')

        # Adding M2M table for field affected on 'Service'
        db.create_table('ops_service_affected', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('service', models.ForeignKey(orm['ops.service'], null=False)),
            ('serviceaffected', models.ForeignKey(orm['ops.serviceaffected'], null=False))
        ))
        db.create_unique('ops_service_affected', ['service_id', 'serviceaffected_id'])


    def backwards(self, orm):

        # Deleting model 'ServiceAffected'
        db.delete_table('ops_serviceaffected')

        # Adding M2M table for field patients on 'Service'
        db.create_table('ops_service_patients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('service', models.ForeignKey(orm['ops.service'], null=False)),
            ('baseperson', models.ForeignKey(orm['common.baseperson'], null=False))
        ))
        db.create_unique('ops_service_patients', ['service_id', 'baseperson_id'])

        # Removing M2M table for field affected on 'Service'
        db.delete_table('ops_service_affected')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 28, 22, 3, 24, 353046)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 28, 22, 3, 24, 352957)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.City']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'map_location': ('common.widgets.LocationField', [], {'max_length': '255', 'blank': 'True'})
        },
        'common.baseperson': {
            'Meta': {'object_name': 'BasePerson'},
            'alternate_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_document': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_name_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'primary_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'})
        },
        'common.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'common.company': {
            'Meta': {'object_name': 'Company'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Address']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rif': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'common.course': {
            'Meta': {'object_name': 'Course'},
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.School']"})
        },
        'common.degree': {
            'Meta': {'object_name': 'Degree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.School']"})
        },
        'common.job': {
            'Meta': {'object_name': 'Job'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'common.person': {
            'Meta': {'object_name': 'Person', '_ormbases': ['common.BasePerson']},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Address']", 'null': 'True', 'through': "orm['common.PersonAddress']", 'symmetrical': 'False'}),
            'baseperson_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.BasePerson']", 'unique': 'True', 'primary_key': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_place': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'born_here'", 'unique': 'True', 'null': 'True', 'to': "orm['common.Address']"}),
            'childs': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['common.BasePerson']"}),
            'civil_state': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Course']", 'null': 'True', 'through': "orm['common.PersonCourse']", 'symmetrical': 'False'}),
            'degrees': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Degree']", 'null': 'True', 'through': "orm['common.PersonDegree']", 'symmetrical': 'False'}),
            'jobs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Job']", 'null': 'True', 'through': "orm['common.PersonJob']", 'symmetrical': 'False'}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'common.personaddress': {
            'Meta': {'object_name': 'PersonAddress'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Address']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Person']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'common.personcourse': {
            'Meta': {'object_name': 'PersonCourse'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Person']"}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'training_course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Course']"})
        },
        'common.persondegree': {
            'Meta': {'object_name': 'PersonDegree'},
            'degree': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Degree']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Person']"}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'common.personjob': {
            'Meta': {'object_name': 'PersonJob'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Job']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Person']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'supervised_set'", 'null': 'True', 'to': "orm['common.BasePerson']"})
        },
        'common.school': {
            'Meta': {'object_name': 'School'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ops.service': {
            'Meta': {'object_name': 'Service'},
            'affected': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ops.ServiceAffected']", 'symmetrical': 'False'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services_created'", 'to': "orm['personal.Firefighter']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'map_location': ('common.widgets.LocationField', [], {'max_length': '255', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'time': ('django.db.models.fields.TimeField', [], {})
        },
        'ops.serviceaffected': {
            'Meta': {'object_name': 'ServiceAffected'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'person_affected': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services_involved'", 'to': "orm['common.BasePerson']"})
        },
        'ops.servicevehicle': {
            'Meta': {'object_name': 'ServiceVehicle'},
            'crew': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'in_services'", 'symmetrical': 'False', 'to': "orm['personal.Firefighter']"}),
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services_drove'", 'to': "orm['personal.Firefighter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services_lead'", 'to': "orm['personal.Firefighter']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vehicles'", 'to': "orm['ops.Service']"}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ops.Vehicle']"})
        },
        'ops.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'personal.firefighter': {
            'Meta': {'ordering': "['-number', 'last_name']", 'object_name': 'Firefighter', '_ormbases': ['common.Person']},
            'blood_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'blood_type_rh': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'profile_picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ranks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['personal.Rank']", 'null': 'True', 'through': "orm['personal.RankChange']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'personal.rank': {
            'Meta': {'object_name': 'Rank'},
            'abrev': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'personal.rankchange': {
            'Meta': {'object_name': 'RankChange'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'firefighter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['personal.Firefighter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank_obtained': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['personal.Rank']"})
        }
    }

    complete_apps = ['ops']
