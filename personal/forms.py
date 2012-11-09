#coding=utf-8
from django import forms
from common.models import PersonTelephoneNumber, TelephoneNumber
from django.core import validators
from django.forms.models import ModelForm
from personal.models import Firefighter


class PersonPhoneForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput, required=False)
    type = forms.ChoiceField(label=u'Tipo', choices=PersonTelephoneNumber.TELEPHONE_TYPE_CHOICES)
    code = forms.CharField(label=u'Código', validators=[validators.MaxLengthValidator(4), validators.RegexValidator(regex="\d\d\d\d")])
    number = forms.CharField(label=u'Número', validators=[validators.MaxLengthValidator(7), validators.RegexValidator(regex="\d\d\d\d\d\d\d")])

    def save(self, instance):
        if self.cleaned_data.get("id", ""):
            phone = instance.persontelephonenumber_set.get(id=self.cleaned_data["id"])
            phone.type = self.data["type"]
            phone.telephone_number.code = self.cleaned_data["code"]
            phone.telephone_number.number = self.cleaned_data["number"]
            phone.telephone_number.save()
            phone.save()
        else:
            tphone = TelephoneNumber(code=self.cleaned_data["code"], number=self.cleaned_data["number"])
            tphone.save()
            phone = PersonTelephoneNumber(person=instance, type=self.cleaned_data["type"], telephone_number=tphone)
            phone.save()


class PartialFirefighterForm(ModelForm):
    class Meta:
        model = Firefighter
        fields = ('profile_picture',)
