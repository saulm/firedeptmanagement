from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       url(r'^$', 'firedeptmanagement.common.views.base', name='base'),
                       url(r'^estadisticas/$', 'firedeptmanagement.ops.views.statistics', name='statistics'),
                       url(r'^estadisticas/plain/$', 'firedeptmanagement.ops.views.plain_statistics', name='plain_statistics'),
                       url(r'^estadisticas/(?P<year>\d+)-(?P<month>\d+)/$', 'firedeptmanagement.ops.views.month_statistics', name='month_statistics'),
                       url(r'^estadisticas/plain/(?P<year>\d+)-(?P<month>\d+)/$', 'firedeptmanagement.ops.views.month_statistics', name='month_statistics_plain'),
                       url(r'^estadisticas/detalle/(?P<year>\d+)-(?P<month>\d+)/$', 'firedeptmanagement.ops.views.month_statistics_detail', name='month_statistics_detail'),
                       url(r'^estadisticas/plain/detalle/(?P<year>\d+)-(?P<month>\d+)/$', 'firedeptmanagement.ops.views.month_statistics_detail', name='month_statistics_detail_plain'),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                       url(r'^directorio/$', 'firedeptmanagement.capitalrelacional.views.search_related', name="directorio"),

                       url(r'^sugerencias/$', 'firedeptmanagement.common.views.create_suggestion', name="create_suggestion"),

                       url(r'^miperfil/$', 'firedeptmanagement.personal.views.user_profile', name="perfil"),
                       url(r'^miperfil/modificar/$', 'firedeptmanagement.personal.views.change_profile_get', name="change_profile_get"),
                       url(r'^miperfil/modificar/basico$', 'firedeptmanagement.personal.views.change_profile', name="change_profile"),

                       url(r'^miperfil/modificar/telefono$', 'firedeptmanagement.personal.views.change_phone', name="change_phone"),

                       url(r'^perfil/(?P<ff_id>\d+)/$', 'firedeptmanagement.personal.views.user_profile', name="perfil_f"),
                       url(r'^eliminar/telefono/(?P<phone_id>\d+)/$', 'firedeptmanagement.personal.views.delete_phone', name="delete_phone"),

                       url(r'^verplanilla/(?P<ff_id>\d+)/$', 'firedeptmanagement.personal.views.view_cnb_form', name="view_cnb_form"),

                       url(r'^servicios/insertar/$', 'firedeptmanagement.ops.views.insert_service', name="insert_service"),
                       url(r'^servicios/$', 'firedeptmanagement.ops.views.list_services', name="list_services"),
                       url(r'^servicio/(?P<service_id>\d+)/$', 'firedeptmanagement.ops.views.view_service', name="view_service"),
                       url(r'^servicio/(?P<service_id>\d+)/image$', 'firedeptmanagement.ops.views.service_upload_image', name="service_upload_image"),
                       
                       
                       url(r'^arrestos/insertar/$', 'firedeptmanagement.ops.views.insert_arrest', name="insert_arrest"),
                       url(r'^arrestos/insertar/pago/$', 'firedeptmanagement.ops.views.insert_arrest_payment', name="insert_arrest_payment"),
                       
                       
                       url(r'^personas/autocompletar/$', 'firedeptmanagement.common.views.autocomplete_person', name="autocomplete_person"),
                       url(r'^bomberos/autocompletar/$', 'firedeptmanagement.personal.views.autocomplete_firefighter', name="autocomplete_firefighter"),
                       url(r'^bomberos/sample/$', 'firedeptmanagement.personal.views.ff_sample', name="firefighter_sample"),
                                              
                       #ADMIN
                       (r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
