from django.apps import AppConfig

class GradesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edu_stats.grades'  # Именно так должно быть в INSTALLED_APPS