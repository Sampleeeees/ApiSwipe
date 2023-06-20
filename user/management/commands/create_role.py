from django.core.management.base import BaseCommand

from user.models import Role

class Command(BaseCommand):
    ROLES = [
        {'name_role': 'Regular user', 'is_regular': True},
        {'name_role': 'Builder', 'is_builder': True},
        {'name_role': 'Notary', 'is_notary': True},
        {'name_role': 'Admin', 'is_admin': True},
        {'name_role': 'Manager', 'is_manager': True}
    ]

    def handle(self, *args, **options):
        for role_data in self.ROLES:
            Role.objects.create(**role_data)
            print(f'{role_data["name_role"]} created')
        print('All roles created')