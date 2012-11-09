# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Person.picture'
        db.alter_column('common_person', 'picture', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True))


    def backwards(self, orm):
        
        # Changing field 'Person.picture'
        db.alter_column('common_person', 'picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))


    models = {
        'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.City']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'map_location': ('firedeptmanagement.common.widgets.LocationField', [], {'max_length': '255', 'blank': 'True'})
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
        'common.companytelephonenumber': {
            'Meta': {'object_name': 'CompanyTelephoneNumber'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'telephone_number': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.TelephoneNumber']"})
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
        'common.persontelephonenumber': {
            'Meta': {'object_name': 'PersonTelephoneNumber'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.BasePerson']"}),
            'telephone_number': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.TelephoneNumber']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'common.school': {
            'Meta': {'object_name': 'School'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'common.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'common.telephonenumber': {
            'Meta': {'object_name': 'TelephoneNumber'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        }
    }

    complete_apps = ['common']
