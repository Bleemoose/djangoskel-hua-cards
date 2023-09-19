from django.apps import AppConfig
import os
from django.core.management import call_command

class CardApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'card_api'

    def ready(self):
        from . import jobs

        if os.environ.get('RUN_MAIN', None) != 'true':
            call_command('create_groups')
            jobs.start_scheduler()