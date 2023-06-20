from django.core.management.base import BaseCommand

from django.utils.translation import gettext_lazy as _
from house.models import House, Floor, Corps, Section
from gallery.models import Gallery
from user.models import User
from flat.models import Flat
from announcement.models import Announcement
from chessboard.models import ChessBoard
class Command(BaseCommand):
    help = _('Створення будинку')

    # Create house
    def handle(self, *args, **options):
        gallery = Gallery.objects.create(text='House gallery')
        builder = User.objects.get(role__is_builder=True)
        house = House.objects.create(
            name='House num.1',
            general_image='house/general_photo/general.jpg',
            address='Odessa',
            map_position='12551 1547 545',
            min_price=12000,
            price_for_m2=250,
            area=12200,
            sea_distance=2,
            builder=builder,
            gallery=gallery
        )
        print('House created')

        # Create floor, section, corps
        for item in range(3):
            section = Section.objects.create(name=f'Section {item}', house=house)
            print(f'Section {item} for {house.name} created')
            floor = Floor.objects.create(name=f'Floor {item}', house=house)
            print(f'Floor {item} for {house.name} created')
            corps = Corps.objects.create(name=f'Corps {item}', house=house)
            print(f'Corps {item} for {house.name} created')

            for f_item in range(2):
                gallery_flat = Gallery.objects.create(text=f'Flat {f_item}')
                flat = Flat.objects.create(
                    room_amount=120,
                    scheme='#',
                    price=120000,
                    square=75,
                    kitchen_square=30,
                    commission=15000,
                    district='Schevchenka 125',
                    micro_district='Prov',
                    house=house,
                    section=section,
                    floor=floor,
                    corps=corps,
                    user=builder,
                    gallery=gallery_flat
                )
                print(f'Flat {f_item} created')
                announcement = Announcement.objects.create(confirm=True, flat=flat)
                print(f'Announcement {f_item} created')

                for chess in range(1):
                    chessboard = ChessBoard.objects.create(
                        house=house,
                        section=section,
                        floor=floor,
                        corps=corps,
                        flat=flat
                    )
                    print(f'ChessBoard {chess} created')

        print('All Created')
