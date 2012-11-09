#!/usr/bin/python
#coding=utf-8
import os
from personal.models import Firefighter
os.environ['DJANGO_SETTINGS_MODULE'] = 'firedeptmanagement.settings'
from opera.models import Servicio
from ops.models import Service, ServiceVehicle, Vehicle


def guess_type(op_s):
    if op_s.fansa != '':
        return op_s.fansa
    if op_s.tipo == "AME":
        return "AME1"
    return op_s.tipo


def get_ff(ff_str):
    Firefighter.objects.get(first_name__startswith=ff_str[0], last_name__istartswith=ff_str[3:])

def func():
    servicios = Servicio.objects.using('opera').all()
    for op_s in servicios:
        service = Service(id=op_s.id,
                          date=op_s.fecha,
                          creation_date=op_s.ingresado,
                          description=op_s.descripcion,
                          time=op_s.hora,
                          service_type=guess_type(op_s),
                          )
        service.save()
        s_vehicle = ServiceVehicle(service=service)
        v = None
        try:
            v = Vehicle.objects.get(name=op_s.unidad)
        except:
            pass
        s_vehicle.vehicle = v



#    ff_str = servicio.jc
#    try:
#        Firefighter.objects.get(first_name__istartswith=ff_str[0], last_name__istartswith=ff_str[3:])
#    except:
#        try:
#            Firefighter.objects.get(primary_email__istartswith=ff_str[0]+ff_str[3:])
#            
#        except:
#            print ff_str

#set([u'K. Mart\xednez',
#     u'M. Ram\xedrez',
#     u'J. Alvarez',
#     u'O. Contamaestre',
#     u'M. Lopez',
#     u'F. Jimenez',
#     u'A. Umerez',
#     u'H. Bar\xe1n',
#     u'M. Belisario',
#     u'L. Rodr\xedguez',
#     u'O. Cntramaestre',
#     u'C. Meneces',
#     u'N. Navan',
#     u'G. P\xe9rez',
#     u'J. Guzman',
#     u'P. Ramos',
#     u'A. Jimenz',
#     u'L. Tocuyo',
#     u'N. Navas',
#     u'V. Duran',
#     u'K. Malav\xe9',
#     u'M. Gomez',
#     u'A. Le\xf3n',
#     u'J. Preira',
#     u'V. Hernandez',
#     u'K. Ju\xe1rez',
#     u'D. Pachon',
#     u'A. Mayz',
#     u'F. Rodrigu\xe9z',
#     u'M. Gonz\xe1lez',
#     u'G. M\xe9ndez',
#     u'A. Maritnez',
#     u'A. Leon',
#     u'M. P\xe9rez',
#     u'D. Phillips',
#     u'F. Rodriguez',
#     u'L. Aurrecochea',
#     u'J. Solva',
#     u'P. Toruella',
#     u'A. S\xe1nchez',
#     u'J. Jim\xe9nez',
#     u'R. Dediego',
#     u'I. Sanchez',
#     u'C. Chag',
#     u'A. Jim\xe9nez'])


#set([u'',
#     u'A. Sanch\xe9z',
#     u'J. Alvarez',
#     u'A. Yallonado',
#     u'C. Cabarela',
#     u'M. Lopez',
#     u'F. Jimenez',
#     u'A. Umerez',
#     u'H. Bar\xe1n',
#     u'O. Comtramaestr',
#     u'M. Ram\xedrez',
#     u'C. Cahng',
#     u'D. Phillip',
#     u'N. Navas',
#     u'K. Malav\xe9',
#     u'M. Gomez',
#     u'P. Torruela',
#     u'A. Yalonardo',
#     u'J.  Rojas',
#     u'O. Contramestre',
#     u'V. Hernandez',
#     u'L. Ferm\xedn',
#     u'K. Ju\xe1rez',
#     u'I. Candiales',
#     u'N. Apellido',
#     u'G. M\xe9ndez',
#     u'J. Figueredo',
#     u'D. Phillips',
#     u'F. Rodriguez',
#     u'V. Hernadez',
#     u'A. S\xe1nchez',
#     u'J. Trevsion',
#     u'I. Sanchez',
#     u'A. Jim\xe9nez'])


