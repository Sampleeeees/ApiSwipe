from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from favorite.models import Favorite
from user.models import User
from announcement.models import Announcement

class Command(BaseCommand):
    help = _('Створення улюблених оголошень')

    # Create Favorite announcement
    def handle(self, *args, **options):
        user_regular = User.objects.filter(role__is_regular=True).first()
        for announ in Announcement.objects.all()[:2]:
            Favorite.objects.create(
                user=user_regular,
                announcement=announ
            )
        print('Favorite created!!!')