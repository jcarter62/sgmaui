from decouple import config
import sgmaui.version

def add_company_info(request):
    organization_name = config('ORGANIZATION_NAME', default='')

    return {'organization_name': organization_name, 'version': sgmaui.version.VERSION}


