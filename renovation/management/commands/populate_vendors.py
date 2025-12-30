from django.core.management.base import BaseCommand
from renovation.models import DropdownChoice


class Command(BaseCommand):
    help = 'Populate vendor options in DropdownChoice model'

    def handle(self, *args, **kwargs):
        vendors = [
            ('allegro', 'Allegro', 'Allegro', 10),
            ('castorama', 'Castorama', 'Castorama', 20),
            ('leroy_merlin', 'Leroy Merlin', 'Leroy Merlin', 30),
            ('brico', 'Brico', 'Brico', 40),
            ('obi', 'OBI', 'OBI', 50),
            ('bricomarche', 'Bricomarché', 'Bricomarché', 60),
            ('other', 'Inny', 'Other', 100),
        ]

        created_count = 0
        for value, label_pl, label_en, order in vendors:
            obj, created = DropdownChoice.objects.get_or_create(
                choice_type='vendor',
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
                        self.style.SUCCESS(f'Created vendor option: {label_en}')
                    )
                except:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created vendor option')
                    )
            else:
                try:
                    self.stdout.write(
                        self.style.WARNING(f'Vendor option already exists: {label_en}')
                    )
                except:
                    self.stdout.write(
                        self.style.WARNING(f'Vendor option already exists')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully populated {created_count} vendor options')
        )
