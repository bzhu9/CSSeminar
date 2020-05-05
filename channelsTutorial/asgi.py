import os
import django
from channels.routing import get_default_application

os.environ['DJANGO_SETTINGS_MODULE'] = "channelsTutorial.settings"
django.setup()

application = get_default_application()