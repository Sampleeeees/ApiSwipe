from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from promotion.models import Promotion
from announcement.models import Announcement

class Command(BaseCommand):
    help = _('Створення продвигу')

    # Create Promotion
    def handle(self, *args, **options):
        Promotion.objects.create(
            highlight=True,
            announcement=Announcement.objects.first()
        )
        Promotion.objects.create(
            turbo=True,
            announcement=Announcement.objects.last()
        )
        print('Promotion created')

