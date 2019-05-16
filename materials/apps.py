from django.apps import AppConfig


class MaterialsConfig(AppConfig):
    name = 'materials'

    def ready(self):
        """Make sure "users" is always up to date with all models."""
        try:
            from django.contrib.auth.models import Group
            from django.contrib.auth.models import Permission
            users = Group.objects.get_or_create(name='users')[0]
            for perm in Permission.objects.filter(
                    content_type__app_label='materials'):
                if perm not in users.permissions.all():
                    users.permissions.add(perm)
        except Exception:
            pass
