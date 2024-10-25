import os
import io
import django
from django.core.management import call_command

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'a_djblog.settings'

# Initialize Django
django.setup()

# Open the output file with UTF-8 encoding
with io.open('mysite_data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', '--indent=2', stdout=f)

"""
#nvm this works
python -Xutf8 manage.py dumpdata --indent=2 --output=mysite_data.json

"""


"""
#
# if migrating troubles incountered
# in python manage.py shell:

from django.contrib.contenttypes.models import ContentType
ContentType.objects.filter(app_label='blog', model='post').exists()
ContentType.objects.filter(app_label='blog').delete()
python manage.py loaddata mysite_data.json 


"""