from django.apps import AppConfig


class BudgetApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budget_api'
    def ready(self):
        import budget_api.signals   # noqa
