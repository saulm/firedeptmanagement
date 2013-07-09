from django.conf import settings 

def config_media(request):
    return {'SITE_HEADER': settings.SITE_HEADER, 'LOGO_URL': settings.LOGO_URL}
