from django.contrib import admin
from firedeptmanagement.common.models import PersonDegree, PersonJob, PersonCourse, PersonAddress, PersonTelephoneNumber, CompanyTelephoneNumber

class PersonDegreeInline(admin.StackedInline):
    model = PersonDegree
    extra = 1

class PersonJobInline(admin.StackedInline):
    model = PersonJob
    extra = 1
    fk_name = 'person'

class PersonCourseInline(admin.StackedInline):
    model = PersonCourse
    extra = 1
    
class PersonAddressInline(admin.StackedInline):
    model = PersonAddress
    extra = 1

class PersonTelephoneNumberInline(admin.StackedInline):
    model = PersonTelephoneNumber
    extra = 1
    raw_id_fields = ("telephone_number",)
    
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonAddressInline, PersonTelephoneNumberInline)

class BasePersonAdmin(admin.ModelAdmin):
    inlines = (PersonTelephoneNumberInline,)

class CompanyTelephoneNumberInline(admin.StackedInline):
    model = CompanyTelephoneNumber
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    inlines = (CompanyTelephoneNumberInline,)
    