from django.core.management.base import BaseCommand
from renovation.models import DropdownChoice


class Command(BaseCommand):
    help = 'Populate wall finish options in DropdownChoice model'

    def handle(self, *args, **kwargs):
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

        created_count = 0
        for value, label_pl, label_en, order in wall_finishes:
            obj, created = DropdownChoice.objects.get_or_create(
                choice_type='wall_finish',
                value=value,
                defaults={
                    'label_pl': label_pl,
                    'label_en': label_en,
                    'display_order': order,
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                try:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created wall finish option: {label_en}')
                    )
                except:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created wall finish option')
                    )
            else:
                try:
                    self.stdout.write(
                        self.style.WARNING(f'Wall finish option already exists: {label_en}')
                    )
                except:
                    self.stdout.write(
                        self.style.WARNING(f'Wall finish option already exists')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully populated {created_count} wall finish options')
        )
