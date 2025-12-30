from django.core.management.base import BaseCommand
from renovation.models import DropdownChoice


class Command(BaseCommand):
    help = 'Populate floor type options in DropdownChoice model'

    def handle(self, *args, **kwargs):
        floor_types = [
            ('plytki', 'Płytki', 'Tiles', 10),
            ('panele', 'Panele', 'Panels', 20),
            ('parkiet', 'Parkiet', 'Parquet', 30),
            ('wykladzina_dywanowa', 'Wykładzina dywanowa', 'Carpet', 40),
        ]

        created_count = 0
        for value, label_pl, label_en, order in floor_types:
            obj, created = DropdownChoice.objects.get_or_create(
                choice_type='floor_type',
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
                        self.style.SUCCESS(f'Created floor type option: {label_en}')
                    )
                except:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created floor type option')
                    )
            else:
                try:
                    self.stdout.write(
                        self.style.WARNING(f'Floor type option already exists: {label_en}')
                    )
                except:
                    self.stdout.write(
                        self.style.WARNING(f'Floor type option already exists')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully populated {created_count} floor type options')
        )
