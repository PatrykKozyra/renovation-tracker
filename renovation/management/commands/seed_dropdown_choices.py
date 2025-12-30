from django.core.management.base import BaseCommand
from renovation.models import DropdownChoice


class Command(BaseCommand):
    help = 'Seed database with dropdown choices from hardcoded model choices'

    def handle(self, *args, **options):
        self.stdout.write('Seeding dropdown choices...')

        # Room types
        room_types = [
            ('salon', 'Salon', 'Living Room', 10),
            ('sypialnia', 'Sypialnia', 'Bedroom', 20),
            ('kuchnia', 'Kuchnia', 'Kitchen', 30),
            ('lazienka', 'Łazienka', 'Bathroom', 40),
            ('ubikacja', 'Ubikacja', 'Toilet', 50),
            ('pokoj_dzieciecy', 'Pokój Dziecięcy', "Children's Room", 60),
            ('biuro', 'Biuro', 'Office', 70),
            ('korytarz', 'Korytarz', 'Hallway', 80),
            ('loggia', 'Loggia', 'Loggia', 90),
        ]

        for value, label_pl, label_en, order in room_types:
            DropdownChoice.objects.get_or_create(
                choice_type='room_type',
                value=value,
                defaults={
                    'label_pl': label_pl,
                    'label_en': label_en,
                    'display_order': order,
                    'is_active': True,
                }
            )
        self.stdout.write(self.style.SUCCESS(f'+ Seeded {len(room_types)} room types'))

        # Floor types
        floor_types = [
            ('plytki', 'Płytki', 'Tiles', 10),
            ('panele', 'Panele', 'Panels', 20),
            ('parkiet', 'Parkiet', 'Parquet', 30),
            ('wykladzina_dywanowa', 'Wykładzina dywanowa', 'Carpet', 40),
        ]

        for value, label_pl, label_en, order in floor_types:
            DropdownChoice.objects.get_or_create(
                choice_type='floor_type',
                value=value,
                defaults={
                    'label_pl': label_pl,
                    'label_en': label_en,
                    'display_order': order,
                    'is_active': True,
                }
            )
        self.stdout.write(self.style.SUCCESS(f'+ Seeded {len(floor_types)} floor types'))

        # Wall finishes
        wall_finishes = [
            ('farba', 'Farba', 'Paint', 10),
            ('tapeta', 'Tapeta', 'Wallpaper', 20),
            ('plytki', 'Płytki', 'Tiles', 30),
            ('fototapeta', 'Fototapeta', 'Photo Wallpaper', 40),
            ('sztukateria', 'Sztukateria', 'Stucco', 50),
            ('boazeria', 'Boazeria', 'Wainscoting', 60),
            ('panele_scienne', 'Panele ścienne', 'Wall Panels', 70),
            ('kamien_dekoracyjny', 'Kamień dekoracyjny', 'Decorative Stone', 80),
            ('beton_architektoniczny', 'Beton architektoniczny', 'Architectural Concrete', 90),
            ('mikrocement', 'Mikrocement', 'Microcement', 100),
        ]

        for value, label_pl, label_en, order in wall_finishes:
            DropdownChoice.objects.get_or_create(
                choice_type='wall_finish',
                value=value,
                defaults={
                    'label_pl': label_pl,
                    'label_en': label_en,
                    'display_order': order,
                    'is_active': True,
                }
            )
        self.stdout.write(self.style.SUCCESS(f'+ Seeded {len(wall_finishes)} wall finishes'))

        # Purchase categories
        purchase_categories = [
            ('equipment', 'Sprzęt', 'Equipment', 10),
            ('materials', 'Materiały', 'Materials', 20),
            ('labor', 'Robocizna', 'Labor', 30),
            ('fuel', 'Paliwo', 'Fuel', 40),
            ('tools', 'Narzędzia', 'Tools', 50),
            ('electrical', 'Elektryka', 'Electrical', 60),
            ('plumbing', 'Hydraulika', 'Plumbing', 70),
            ('other', 'Inne', 'Other', 80),
        ]

        for value, label_pl, label_en, order in purchase_categories:
            DropdownChoice.objects.get_or_create(
                choice_type='purchase_category',
                value=value,
                defaults={
                    'label_pl': label_pl,
                    'label_en': label_en,
                    'display_order': order,
                    'is_active': True,
                }
            )
        self.stdout.write(self.style.SUCCESS(f'+ Seeded {len(purchase_categories)} purchase categories'))

        self.stdout.write(self.style.SUCCESS('\n+ All dropdown choices seeded successfully!'))
