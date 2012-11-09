#!/usr/bin/python
#coding=utf-8
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'firedeptmanagement.settings'

from personal.models import Firefighter
from common.models import TelephoneNumber, PersonTelephoneNumber
from datetime import date


def main():
    f = open(sys.argv[1], 'r')
    for line in f.readlines():
        #carnet;Nombre1;Nombre2;apellido1;apellido2;cedula;genero;email1;fechanac;factorsangre;rhsangre;tlf_casa;tlf_cel;email2
        f_list = line.split(";")
        f = Firefighter()
        print f_list[0]
        f.number = int(f_list[0])
        f.first_name = f_list[1]
        f.last_name = f_list[3]

        if f_list[2]:
            f.first_name_2 = f_list[2]
        if f_list[4]:
            f.last_name_2 = f_list[4]
        if f_list[5]:
            f.id_document = f_list[5]
        if f_list[6]:
            f.gender = f_list[6]
        if f_list[7]:
            f.primary_email = f_list[7]
        if f_list[8]:
            fn_list = f_list[8].split("-")
            f.birth_date = date(int(fn_list[0]), int(fn_list[1]), int(fn_list[2]))
        if f_list[9]:
            f.blood_type = f_list[9]
        if f_list[10]:
            f.blood_type_rh = f_list[10]
        if f_list[13]:
            f.alternate_email = f_list[13]
        f.save()

        if f_list[11]:
            fone_list = f_list[11].split("-")
            t = TelephoneNumber()
            t.code = fone_list[0]
            t.number = fone_list[1]
            t.save()
            pt = PersonTelephoneNumber(person=f, telephone_number=t, main=False, type='C')
            pt.save()
        if f_list[12]:
            fone_list = f_list[12].split("-")
            t = TelephoneNumber()
            t.code = fone_list[0]
            t.number = fone_list[1]
            t.save()
            pt = PersonTelephoneNumber(person=f, telephone_number=t, main=True, type='M')
            pt.save()

if __name__ == '__main__':
    main()
