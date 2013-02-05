from django.contrib import admin
from firedeptmanagement.personal.models import Firefighter, Rank, RankChange, Condition, ConditionChange
from firedeptmanagement.common.models import TelephoneNumber, Degree, Course, School, Company, Address, City,\
    BasePerson, Person
from firedeptmanagement.common.admin import PersonDegreeInline, PersonCourseInline, PersonJobInline, PersonAddressInline, PersonTelephoneNumberInline,\
    PersonAdmin, BasePersonAdmin
from personal.models import Condecoration, CondecorationAward, FirefighterHoliday
from sorl.thumbnail.admin import  AdminImageMixin

class RankChangeInline(admin.StackedInline):
    model = RankChange
    extra = 1

class ConditionChangeInline(admin.StackedInline):
    model = ConditionChange
    extra = 1

class CondecorationAwardInline(admin.StackedInline):
    model = CondecorationAward
    extra = 1

class FirefighterHolidayInline(admin.StackedInline):
    list_display = ('firefighter', 'start_at', 'end_at')
    list_display_links = ('firefighter', 'start_at', 'end_at')
    model = FirefighterHoliday
    extra = 1

class FirefighterHolidayAdmin(admin.ModelAdmin):
    list_display = ('firefighter', 'start_at', 'end_at')
    list_display_links = ('firefighter', 'start_at', 'end_at')
        

class FirefighterAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'number', 'id_document', 'primary_email', 'alternate_email')
    list_display_links = ('number', 'last_name', 'first_name')
    inlines = (PersonDegreeInline, PersonCourseInline, PersonJobInline, PersonAddressInline, PersonTelephoneNumberInline, ConditionChangeInline, RankChangeInline, CondecorationAwardInline, FirefighterHolidayInline)

admin.site.register(Firefighter, FirefighterAdmin)
admin.site.register(TelephoneNumber)
admin.site.register(Degree)
admin.site.register(Course)
admin.site.register(School)
admin.site.register(Rank)
admin.site.register(RankChange)
admin.site.register(Company)
admin.site.register(Condition)
admin.site.register(Address)
admin.site.register(City)
admin.site.register(ConditionChange)
admin.site.register(Condecoration)
admin.site.register(FirefighterHoliday, FirefighterHolidayAdmin)
admin.site.register(CondecorationAward)
admin.site.register(BasePerson, BasePersonAdmin)
admin.site.register(Person, PersonAdmin)

