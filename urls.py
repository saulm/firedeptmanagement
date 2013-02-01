from django.conf.urls import patterns, include, url
from django.conf import settings
from settings import MEDIA_ROOT
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'firedeptmanagement.frontpage.views.frontpage', name='frontpage'),
                       url(r'^gestion/$', 'firedeptmanagement.common.views.base', name='base'),
                       url(r'^gestion/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                       url(r'^gestion/directorio/$', 'firedeptmanagement.capitalrelacional.views.search_related', name="directorio"),

                       url(r'^gestion/sugerencias/$', 'firedeptmanagement.common.views.create_suggestion', name="create_suggestion"),

                       url(r'^gestion/miperfil/$', 'firedeptmanagement.personal.views.user_profile', name="perfil"),
                       url(r'^gestion/miperfil/modificar/$', 'firedeptmanagement.personal.views.change_profile_get', name="change_profile_get"),
                       url(r'^gestion/miperfil/modificar/basico$', 'firedeptmanagement.personal.views.change_profile', name="change_profile"),

                       url(r'^gestion/miperfil/modificar/telefono$', 'firedeptmanagement.personal.views.change_phone', name="change_phone"),

                       url(r'^gestion/perfil/(?P<ff_id>\d+)/$', 'firedeptmanagement.personal.views.user_profile', name="perfil_f"),
                       url(r'^gestion/eliminar/telefono/(?P<phone_id>\d+)/$', 'firedeptmanagement.personal.views.delete_phone', name="delete_phone"),

                       url(r'^gestion/verplanilla/(?P<ff_id>\d+)/$', 'firedeptmanagement.personal.views.view_cnb_form', name="view_cnb_form"),

                       url(r'^gestion/servicios/insertar/$', 'firedeptmanagement.ops.views.insert_service', name="insert_service"),
                       url(r'^gestion/servicios/$', 'firedeptmanagement.ops.views.list_services', name="list_services"),
                       url(r'^gestion/servicio/(?P<service_id>\d+)/$', 'firedeptmanagement.ops.views.view_service', name="view_service"),
                       
                       url(r'^gestion/arrestos/insertar/$', 'firedeptmanagement.ops.views.insert_arrest', name="insert_arrest"),
                       
                       
                       url(r'^gestion/personas/autocompletar/$', 'firedeptmanagement.common.views.autocomplete_person', name="autocomplete_person"),
                       url(r'^gestion/bomberos/autocompletar/$', 'firedeptmanagement.personal.views.autocomplete_firefighter', name="autocomplete_firefighter"),

                       #ADMIN
                       (r'^gestion/admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
