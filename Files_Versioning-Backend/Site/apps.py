from django.apps import AppConfig
from GRPC.client import connect_storage


class SiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Site'

    def ready(self):
        pass
        connect_storage()
