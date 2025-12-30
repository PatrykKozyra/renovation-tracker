from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User


class Property(models.Model):
    """Property/Flat being renovated - top-level hierarchy"""

    # Short name for easy identification
    name = models.CharField(
        max_length=100,
        verbose_name=_('Nazwa')
    )

    # Full address
    street_address = models.CharField(
        max_length=200,
        verbose_name=_('Ulica i numer')
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name=_('Kod pocztowy')
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_('Miasto')
    )
    country = models.CharField(
        max_length=100,
        default='Poland',
        verbose_name=_('Kraj')
    )

    # Optional fields
    description = models.TextField(
        blank=True,
        verbose_name=_('Opis')
    )

    # Ownership/access
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name=_('Właściciel')
    )

    # Status tracking
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktywny')
    )
    renovation_start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Data rozpoczęcia remontu')
    )
    renovation_end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Data zakończenia remontu')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Data aktualizacji')
    )

    class Meta:
        verbose_name = _('Nieruchomość')
        verbose_name_plural = _('Nieruchomości')
        ordering = ['-is_active', '-created_at']
        indexes = [
            models.Index(fields=['owner', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.street_address}, {self.city})"

    @property
    def full_address(self):
        """Get complete formatted address"""
        return f"{self.street_address}, {self.postal_code} {self.city}, {self.country}"


class PurchaseCategory(models.Model):
    """Category for renovation purchases"""

    CATEGORY_CHOICES = [
        ('equipment', _('Sprzęt')),  # Equipment
        ('materials', _('Materiały')),  # Materials
        ('labor', _('Robocizna')),  # Labor
        ('fuel', _('Paliwo')),  # Fuel
        ('tools', _('Narzędzia')),  # Tools
        ('electrical', _('Elektryka')),  # Electrical
        ('plumbing', _('Hydraulika')),  # Plumbing
        ('other', _('Inne')),  # Other
    ]

    name = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        unique=True,
        verbose_name=_('Nazwa kategorii')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Opis')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )

    class Meta:
        verbose_name = _('Kategoria zakupu')
        verbose_name_plural = _('Kategorie zakupów')
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class Purchase(models.Model):
    """Record of a purchase made for the renovation"""

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name=_('Nieruchomość')
    )
    category = models.ForeignKey(
        PurchaseCategory,
        on_delete=models.PROTECT,
        related_name='purchases',
        verbose_name=_('Kategoria')
    )
    date = models.DateField(
        verbose_name=_('Data zakupu')
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Kwota')
    )
    vendor = models.CharField(
        max_length=200,
        verbose_name=_('Sklep/Dostawca')
    )
    description = models.TextField(
        verbose_name=_('Opis')
    )
    receipt_photo = models.ImageField(
        upload_to='receipts/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_('Zdjęcie paragonu')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notatki')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Data aktualizacji')
    )

    class Meta:
        verbose_name = _('Zakup')
        verbose_name_plural = _('Zakupy')
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['category', '-date']),
        ]

    def __str__(self):
        return f"{self.date} - {self.vendor} - {self.amount} PLN"


class Room(models.Model):
    """Rooms in the property being renovated"""

    ROOM_CHOICES = [
        ('salon', _('Salon')),  # Living room
        ('sypialnia', _('Sypialnia')),  # Bedroom
        ('kuchnia', _('Kuchnia')),  # Kitchen
        ('lazienka', _('Łazienka')),  # Bathroom
        ('ubikacja', _('Ubikacja')),  # Toilet
        ('pokoj_dzieciecy', _('Pokój Dziecięcy')),  # Children's room
        ('biuro', _('Biuro')),  # Office
        ('korytarz', _('Korytarz')),  # Hallway
        ('loggia', _('Loggia')),  # Loggia
    ]

    FLOOR_TYPE_CHOICES = [
        ('plytki', _('Płytki')),
        ('panele', _('Panele')),
        ('parkiet', _('Parkiet')),
        ('wykladzina_dywanowa', _('Wykładzina dywanowa')),
    ]

    WALL_FINISH_CHOICES = [
        ('farba', _('Farba')),
        ('tapeta', _('Tapeta')),
        ('plytki', _('Płytki')),
        ('fototapeta', _('Fototapeta')),
        ('sztukateria', _('Sztukateria')),
        ('boazeria', _('Boazeria')),
        ('panele_scienne', _('Panele ścienne')),
        ('kamien_dekoracyjny', _('Kamień dekoracyjny')),
        ('beton_architektoniczny', _('Beton architektoniczny')),
        ('mikrocement', _('Mikrocement')),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name=_('Nieruchomość')
    )
    name = models.CharField(
        max_length=50,
        choices=ROOM_CHOICES,
        verbose_name=_('Typ pomieszczenia')
    )
    short_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Krótka nazwa')
    )

    # Dimensions
    width = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Szerokość (m)')
    )
    length = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Długość (m)')
    )
    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Wysokość (m)')
    )
    square_meters = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Powierzchnia (m²)')
    )

    # Finishes
    floor_type = models.CharField(
        max_length=50,
        choices=FLOOR_TYPE_CHOICES,
        blank=True,
        verbose_name=_('Typ podłogi')
    )
    wall_finishes = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Wykończenie ścian'),
        help_text=_('Oddziel przecinkami, np: farba,tapeta')
    )

    # Status and progress
    current_status = models.TextField(
        blank=True,
        verbose_name=_('Aktualny status')
    )
    future_plans = models.TextField(
        blank=True,
        verbose_name=_('Plany na przyszłość')
    )
    progress_notes = models.TextField(
        blank=True,
        verbose_name=_('Notatki o postępie')
    )
    progress_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Postęp (%)')
    )

    description = models.TextField(
        blank=True,
        verbose_name=_('Opis')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Data aktualizacji')
    )

    class Meta:
        verbose_name = _('Pomieszczenie')
        verbose_name_plural = _('Pomieszczenia')
        ordering = ['property', 'name']
        unique_together = [['property', 'name']]

    def __str__(self):
        if self.short_name:
            return f"{self.property.name} - {self.short_name}"
        return f"{self.property.name} - {self.get_name_display()}"

    def get_display_name(self):
        """Get the display name for the room"""
        if self.short_name:
            return self.short_name
        return self.get_name_display()


class RoomProgress(models.Model):
    """Track progress photos and updates for each room"""

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='progress_entries',
        verbose_name=_('Pomieszczenie')
    )
    date = models.DateField(
        verbose_name=_('Data')
    )
    description = models.TextField(
        verbose_name=_('Opis postępu')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Dodatkowe notatki')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Data aktualizacji')
    )

    class Meta:
        verbose_name = _('Postęp prac')
        verbose_name_plural = _('Postępy prac')
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['room', '-date']),
            models.Index(fields=['-date']),
        ]

    def __str__(self):
        return f"{self.room} - {self.date}"


class RoomProgressPhoto(models.Model):
    """Photos associated with room progress entries"""

    progress = models.ForeignKey(
        RoomProgress,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_('Postęp')
    )
    photo = models.ImageField(
        upload_to='progress/%Y/%m/',
        verbose_name=_('Zdjęcie')
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Podpis')
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data przesłania')
    )

    class Meta:
        verbose_name = _('Zdjęcie postępu')
        verbose_name_plural = _('Zdjęcia postępu')
        ordering = ['uploaded_at']

    def __str__(self):
        return f"{self.progress} - {self.caption or 'Photo'}"


class WorkSession(models.Model):
    """Track work sessions/visits to the renovation site"""

    date = models.DateField(
        verbose_name=_('Data')
    )
    start_time = models.TimeField(
        verbose_name=_('Godzina rozpoczęcia')
    )
    end_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name=_('Godzina zakończenia')
    )
    notes = models.TextField(
        verbose_name=_('Notatki')
    )
    rooms_worked_on = models.ManyToManyField(
        Room,
        blank=True,
        related_name='work_sessions',
        verbose_name=_('Pomieszczenia')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Data aktualizacji')
    )

    class Meta:
        verbose_name = _('Sesja pracy')
        verbose_name_plural = _('Sesje pracy')
        ordering = ['-date', '-start_time']
        indexes = [
            models.Index(fields=['-date', '-start_time']),
        ]

    def __str__(self):
        end = f" - {self.end_time}" if self.end_time else ""
        return f"{self.date} {self.start_time}{end}"

    @property
    def duration(self):
        """Calculate duration of work session"""
        if self.end_time and self.start_time:
            from datetime import datetime, timedelta
            start = datetime.combine(self.date, self.start_time)
            end = datetime.combine(self.date, self.end_time)
            if end < start:
                end += timedelta(days=1)
            return end - start
        return None


class ElectricalCircuit(models.Model):
    """Document electrical circuits and their connections"""

    circuit_name = models.CharField(
        max_length=100,
        verbose_name=_('Nazwa obwodu')
    )
    breaker_number = models.CharField(
        max_length=20,
        verbose_name=_('Numer bezpiecznika/wyłącznika')
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name='circuits',
        verbose_name=_('Pomieszczenie')
    )
    connected_appliances = models.TextField(
        verbose_name=_('Podłączone urządzenia'),
        help_text=_('Lista urządzeń podłączonych do tego obwodu')
    )
    amperage = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Amperaż (A)'),
        help_text=_('Natężenie prądu w amperach')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notatki')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Data aktualizacji')
    )

    class Meta:
        verbose_name = _('Obwód elektryczny')
        verbose_name_plural = _('Obwody elektryczne')
        ordering = ['breaker_number', 'circuit_name']
        indexes = [
            models.Index(fields=['room']),
            models.Index(fields=['breaker_number']),
        ]

    def __str__(self):
        return f"{self.breaker_number} - {self.circuit_name} ({self.room})"


class DropdownChoice(models.Model):
    """Manage dropdown options dynamically"""

    CHOICE_TYPE_CHOICES = [
        ('room_type', _('Typ pomieszczenia')),
        ('floor_type', _('Typ podłogi')),
        ('wall_finish', _('Wykończenie ścian')),
        ('purchase_category', _('Kategoria zakupu')),
    ]

    choice_type = models.CharField(
        max_length=50,
        choices=CHOICE_TYPE_CHOICES,
        verbose_name=_('Typ pola')
    )
    value = models.CharField(
        max_length=100,
        verbose_name=_('Wartość (klucz)')
    )
    label_pl = models.CharField(
        max_length=200,
        verbose_name=_('Etykieta (PL)')
    )
    label_en = models.CharField(
        max_length=200,
        verbose_name=_('Etykieta (EN)')
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Kolejność wyświetlania')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktywny')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Data aktualizacji')
    )

    class Meta:
        verbose_name = _('Opcja rozwijanej listy')
        verbose_name_plural = _('Opcje rozwijanej listy')
        ordering = ['choice_type', 'display_order', 'label_pl']
        unique_together = [['choice_type', 'value']]
        indexes = [
            models.Index(fields=['choice_type', 'is_active']),
        ]

    def __str__(self):
        return f"{self.get_choice_type_display()} - {self.label_pl}"

    @classmethod
    def get_choices_for_type(cls, choice_type):
        """Get active choices for a specific dropdown type"""
        choices = cls.objects.filter(
            choice_type=choice_type,
            is_active=True
        ).order_by('display_order', 'label_pl')
        return [(choice.value, choice.label_pl) for choice in choices]


class Equipment(models.Model):
    """Equipment and tools used in renovations"""

    CONDITION_CHOICES = [
        ('ok', _('OK - Sprawny')),
        ('broken', _('Zepsuty')),
        ('missing_parts', _('Brakuje części')),
    ]

    # Basic information
    name = models.CharField(
        max_length=200,
        verbose_name=_('Nazwa narzędzia/sprzętu')
    )
    purpose = models.TextField(
        verbose_name=_('Przeznaczenie'),
        help_text=_('Do czego głównie służy to narzędzie/sprzęt')
    )
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='ok',
        verbose_name=_('Stan techniczny')
    )

    # Purchase information (optional if old equipment)
    is_old = models.BooleanField(
        default=False,
        verbose_name=_('Stary sprzęt'),
        help_text=_('Zaznacz jeśli nie posiadasz danych o zakupie')
    )
    purchase_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Data zakupu')
    )
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Cena zakupu')
    )
    vendor = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Miejsce zakupu')
    )
    receipt_photo = models.ImageField(
        upload_to='equipment/receipts/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_('Zdjęcie paragonu')
    )

    # Sold information
    is_sold = models.BooleanField(
        default=False,
        verbose_name=_('Sprzedany')
    )
    sold_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Data sprzedaży')
    )
    sold_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Cena sprzedaży')
    )

    # Ownership
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='equipment',
        verbose_name=_('Właściciel')
    )

    # Metadata
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notatki')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Data aktualizacji')
    )

    class Meta:
        verbose_name = _('Narzędzie/Sprzęt')
        verbose_name_plural = _('Narzędzia/Sprzęt')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'is_sold']),
            models.Index(fields=['is_sold', '-created_at']),
        ]

    def __str__(self):
        status = _('(sprzedany)') if self.is_sold else ''
        return f"{self.name} {status}".strip()

    @property
    def current_assignment(self):
        """Get current active property assignment"""
        return self.assignments.filter(end_date__isnull=True).first()

    @property
    def is_assigned(self):
        """Check if equipment is currently assigned to a property"""
        return self.current_assignment is not None


class EquipmentPhoto(models.Model):
    """Photos of equipment (max 5 per equipment)"""

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_('Sprzęt')
    )
    photo = models.ImageField(
        upload_to='equipment/photos/%Y/%m/',
        verbose_name=_('Zdjęcie')
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Opis zdjęcia')
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data przesłania')
    )

    class Meta:
        verbose_name = _('Zdjęcie sprzętu')
        verbose_name_plural = _('Zdjęcia sprzętu')
        ordering = ['uploaded_at']

    def __str__(self):
        return f"{self.equipment.name} - {self.caption or 'Zdjęcie'}"


class EquipmentAssignment(models.Model):
    """Track equipment assignment to properties with history"""

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_('Sprzęt')
    )
    assigned_property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='equipment_assignments',
        verbose_name=_('Nieruchomość')
    )
    start_date = models.DateField(
        verbose_name=_('Data przypisania')
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Data zwolnienia'),
        help_text=_('Puste jeśli sprzęt nadal jest przypisany')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notatki')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )

    class Meta:
        verbose_name = _('Przypisanie sprzętu')
        verbose_name_plural = _('Przypisania sprzętu')
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['equipment', 'end_date']),
            models.Index(fields=['assigned_property', 'end_date']),
        ]

    def __str__(self):
        status = _('aktywne') if not self.end_date else f"{_('do')} {self.end_date}"
        return f"{self.equipment.name} → {self.assigned_property.name} ({status})"

    @property
    def is_active(self):
        """Check if assignment is currently active"""
        return self.end_date is None
