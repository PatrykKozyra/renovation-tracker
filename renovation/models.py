from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal


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

    name = models.CharField(
        max_length=50,
        choices=ROOM_CHOICES,
        unique=True,
        verbose_name=_('Nazwa pomieszczenia')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Opis')
    )
    square_meters = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Powierzchnia (m²)')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Data utworzenia')
    )

    class Meta:
        verbose_name = _('Pomieszczenie')
        verbose_name_plural = _('Pomieszczenia')
        ordering = ['name']

    def __str__(self):
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
