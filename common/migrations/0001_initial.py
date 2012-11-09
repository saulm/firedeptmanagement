# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TelephoneNumber'
        db.create_table('common_telephonenumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=7)),
        ))
        db.send_create_signal('common', ['TelephoneNumber'])

        # Adding model 'City'
        db.create_table('common_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('common', ['City'])

        # Adding model 'Address'
        db.create_table('common_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.City'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('map_location', self.gf('firedeptmanagement.common.widgets.LocationField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('common', ['Address'])

        # Adding model 'School'
        db.create_table('common_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('common', ['School'])

        # Adding model 'Degree'
        db.create_table('common_degree', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.School'])),
        ))
        db.send_create_signal('common', ['Degree'])

        # Adding model 'Course'
        db.create_table('common_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.School'])),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('common', ['Course'])

        # Adding model 'Company'
        db.create_table('common_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Address'], null=True, blank=True)),
            ('rif', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['Company'])

        # Adding model 'Job'
        db.create_table('common_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Company'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('common', ['Job'])

        # Adding model 'BasePerson'
        db.create_table('common_baseperson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('first_name_2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name_2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('id_document', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('primary_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('alternate_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['BasePerson'])

        # Adding model 'PersonTelephoneNumber'
        db.create_table('common_persontelephonenumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.BasePerson'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('telephone_number', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.TelephoneNumber'])),
            ('main', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('common', ['PersonTelephoneNumber'])

        # Adding model 'CompanyTelephoneNumber'
        db.create_table('common_companytelephonenumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Company'])),
            ('telephone_number', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.TelephoneNumber'])),
            ('main', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('common', ['CompanyTelephoneNumber'])

        # Adding model 'Person'
        db.create_table('common_person', (
            ('baseperson_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.BasePerson'], unique=True, primary_key=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('birth_place', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='born_here', unique=True, null=True, to=orm['common.Address'])),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('civil_state', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['Person'])

        # Adding M2M table for field childs on 'Person'
        db.create_table('common_person_childs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['common.person'], null=False)),
            ('baseperson', models.ForeignKey(orm['common.baseperson'], null=False))
        ))
        db.create_unique('common_person_childs', ['person_id', 'baseperson_id'])

        # Adding model 'PersonAddress'
        db.create_table('common_personaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Person'])),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Address'])),
        ))
        db.send_create_signal('common', ['PersonAddress'])

        # Adding model 'PersonDegree'
        db.create_table('common_persondegree', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Person'])),
            ('degree', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Degree'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['PersonDegree'])

        # Adding model 'PersonCourse'
        db.create_table('common_personcourse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Person'])),
            ('training_course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Course'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['PersonCourse'])

        # Adding model 'PersonJob'
        db.create_table('common_personjob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Person'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Job'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('supervisor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='supervised_set', null=True, to=orm['common.BasePerson'])),
        ))
        db.send_create_signal('common', ['PersonJob'])

        # Adding model 'Suggestion'
        db.create_table('common_suggestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('common', ['Suggestion'])


    def backwards(self, orm):
        
        # Deleting model 'TelephoneNumber'
        db.delete_table('common_telephonenumber')

        # Deleting model 'City'
        db.delete_table('common_city')

        # Deleting model 'Address'
        db.delete_table('common_address')

        # Deleting model 'School'
        db.delete_table('common_school')

        # Deleting model 'Degree'
        db.delete_table('common_degree')

        # Deleting model 'Course'
        db.delete_table('common_course')

        # Deleting model 'Company'
        db.delete_table('common_company')

        # Deleting model 'Job'
        db.delete_table('common_job')

        # Deleting model 'BasePerson'
        db.delete_table('common_baseperson')

        # Deleting model 'PersonTelephoneNumber'
        db.delete_table('common_persontelephonenumber')

        # Deleting model 'CompanyTelephoneNumber'
        db.delete_table('common_companytelephonenumber')

        # Deleting model 'Person'
        db.delete_table('common_person')

        # Removing M2M table for field childs on 'Person'
        db.delete_table('common_person_childs')

        # Deleting model 'PersonAddress'
        db.delete_table('common_personaddress')

        # Deleting model 'PersonDegree'
        db.delete_table('common_persondegree')

        # Deleting model 'PersonCourse'
        db.delete_table('common_personcourse')

        # Deleting model 'PersonJob'
        db.delete_table('common_personjob')

        # Deleting model 'Suggestion'
        db.delete_table('common_suggestion')


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
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
