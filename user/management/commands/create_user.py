from django.core.management.base import BaseCommand
from allauth.account.models import EmailAddress
from django.utils.translation import gettext_lazy as _
from user.models import User, Role

class Command(BaseCommand):
    help = _('Створення новий користувачів')

    def handle(self, *args, **options):
        # Create Admin user
        role_admin = Role.objects.get(is_admin=True)
        admin = User.objects.create(
            name='admin',
            surname='admin',
            is_superuser=True,
            email='admin@admin.com',
            phone_number=1234568,
            role=role_admin
        )
        admin.set_password('swipe123')
        admin.save()
        print('Admin created')

        # Enter a admin email for login
        email_admin = EmailAddress.objects.create(
            email=admin.email,
            verified=True,
            primary=True,
            user=admin
        )
        email_admin.save()
        print('Admin email verified')

        # Create Builder user
        role_builder = Role.objects.get(is_builder=True)
        builder = User.objects.create(
            name='builder',
            surname='builder',
            email='builder@builder.com',
            phone_number=4569875,
            role=role_builder
        )
        builder.set_password('swipe123')
        builder.save()
        print('Builder created')

        # Enter builder email for login
        email_builder = EmailAddress.objects.create(
            email=builder.email,
            verified=True,
            primary=True,
            user=builder
        )
        email_builder.save()
        print('Builder email verified')

        # Create Notary user
        role_notary = Role.objects.get(is_notary=True)
        notary = User.objects.create(
            name='notary',
            surname='notary',
            email='notary@notary.com',
            phone_number=126547,
            role=role_notary
        )
        notary.set_password('swipe123')
        notary.save()
        print('Notary created')

        # Enter notary email for login
        email_notary = EmailAddress.objects.create(
            email=notary.email,
            verified=True,
            primary=True,
            user=notary
        )
        email_notary.save()
        print('Notary email verified')

        # Create Manager user
        role_manager = Role.objects.get(is_manager=True)
        manager = User.objects.create(
            name='manager',
            surname='manager',
            email='manager@manager.com',
            phone_number=458965,
            role=role_manager
        )
        manager.set_password('swipe123')
        manager.save()
        print('Manager created')

        # Enter Manager email for login
        email_manager = EmailAddress.objects.create(
            email=manager.email,
            verified=True,
            primary=True,
            user=manager
        )
        email_manager.save()
        print('Manager email verified')

        # Create Regular user
        role_regular = Role.objects.get(name_role='Regular user')
        regular = User.objects.create(
            name='regular',
            surname='regular',
            email='regular@regular.com',
            phone_number=4566589,
            role=role_regular
        )
        regular.set_password('swipe123')
        regular.save()
        print('Regular created')

        # Enter regular email for login
        email_regular = EmailAddress.objects.create(
            email=regular.email,
            verified=True,
            primary=True,
            user=regular
        )
        email_regular.save()
        print('Regular email verified')






