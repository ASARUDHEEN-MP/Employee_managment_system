# Employee_auths/apps.py
from django.apps import AppConfig

class EmployeeAuthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Employee_auths'

    def ready(self):
        import Employee_auths.signals  # Ensure the signals are imported
