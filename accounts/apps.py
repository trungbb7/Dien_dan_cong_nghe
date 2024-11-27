<<<<<<< HEAD
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals
=======
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals
>>>>>>> 97ee8979c26f5f129f58b20f34ac71188cb18c3b
