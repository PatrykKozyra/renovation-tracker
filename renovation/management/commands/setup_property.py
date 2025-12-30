from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from renovation.models import Property, Purchase, Room


class Command(BaseCommand):
    help = 'Set up first property and link existing data'

    def handle(self, *args, **options):
        # Get the first user (admin)
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
            return

        # Check if property already exists
        existing_property = Property.objects.first()
        if existing_property:
            self.stdout.write(self.style.WARNING(f'Property already exists: {existing_property}'))
            property_obj = existing_property
        else:
            # Create default property
            property_obj = Property.objects.create(
                name='My Renovation Project',
                street_address='Test Street 1/2',
                postal_code='30-922',
                city='Kraków',
                country='Poland',
                owner=user,
                description='First renovation property'
            )
            self.stdout.write(self.style.SUCCESS(f'Created property: {property_obj}'))

        # Link existing purchases to this property
        purchases_updated = Purchase.objects.filter(property__isnull=True).update(property=property_obj)
        self.stdout.write(self.style.SUCCESS(f'Linked {purchases_updated} purchases to property'))

        # Link existing rooms to this property
        rooms_updated = Room.objects.filter(property__isnull=True).update(property=property_obj)
        self.stdout.write(self.style.SUCCESS(f'Linked {rooms_updated} rooms to property'))

        self.stdout.write(self.style.SUCCESS('Setup complete!'))
        self.stdout.write(f'Property: {property_obj.full_address}')
