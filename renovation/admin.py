from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Sum, Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.admin import AdminSite
from datetime import timedelta
from .models import (
    PurchaseCategory,
    Purchase,
    Room,
    RoomProgress,
    RoomProgressPhoto,
    WorkSession,
    ElectricalCircuit
)


class RenovationAdminSite(AdminSite):
    site_header = _('Panel Administracyjny Remontu')
    site_title = _('Remont')
    index_title = _('Zarządzanie remontem')

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Total spending
        total_spent = Purchase.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        purchase_count = Purchase.objects.count()

        # Progress entries
        progress_entries_count = RoomProgress.objects.count()

        # Work sessions
        work_sessions_count = WorkSession.objects.count()
        work_sessions = WorkSession.objects.all()
        total_duration = timedelta()
        for session in work_sessions:
            if session.duration:
                total_duration += session.duration
        total_work_hours = total_duration.total_seconds() / 3600

        # Photos
        total_photos = RoomProgressPhoto.objects.count()

        # Category spending
        categories = PurchaseCategory.objects.annotate(
            total=Sum('purchases__amount')
        ).order_by('-total')
        category_spending = []
        for cat in categories:
            if cat.total:
                category_spending.append({
                    'name': cat.get_name_display(),
                    'total': cat.total
                })

        # Room progress
        rooms = Room.objects.annotate(
            entries=Count('progress_entries')
        ).order_by('-entries')
        room_progress = []
        for room in rooms:
            if room.entries > 0:
                room_progress.append({
                    'name': room.get_name_display(),
                    'entries': room.entries
                })

        extra_context.update({
            'total_spent': total_spent,
            'purchase_count': purchase_count,
            'progress_entries_count': progress_entries_count,
            'work_sessions_count': work_sessions_count,
            'total_work_hours': total_work_hours,
            'total_photos': total_photos,
            'category_spending': category_spending,
            'room_progress': room_progress,
        })

        return super().index(request, extra_context)


# Create custom admin site instance
renovation_admin_site = RenovationAdminSite(name='renovation_admin')


@admin.register(PurchaseCategory)
class PurchaseCategoryAdmin(admin.ModelAdmin):
    list_display = ['get_name_display_custom', 'description', 'get_purchase_count', 'get_total_spent', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'get_purchase_count', 'get_total_spent']

    fieldsets = (
        (_('Podstawowe informacje'), {
            'fields': ('name', 'description')
        }),
        (_('Statystyki'), {
            'fields': ('get_purchase_count', 'get_total_spent'),
            'classes': ('collapse',)
        }),
        (_('Metadane'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_name_display_custom(self, obj):
        return obj.get_name_display()
    get_name_display_custom.short_description = _('Kategoria')
    get_name_display_custom.admin_order_field = 'name'

    def get_purchase_count(self, obj):
        count = obj.purchases.count()
        return format_html('<strong>{}</strong>', count)
    get_purchase_count.short_description = _('Liczba zakupów')

    def get_total_spent(self, obj):
        total = obj.purchases.aggregate(Sum('amount'))['amount__sum'] or 0
        return format_html('<strong>{:.2f} PLN</strong>', total)
    get_total_spent.short_description = _('Suma wydatków')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['date', 'vendor', 'category', 'amount_display', 'description_short', 'has_receipt']
    list_filter = ['category', 'date', 'vendor']
    search_fields = ['vendor', 'description', 'notes']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'receipt_preview']
    list_per_page = 50

    fieldsets = (
        (_('Podstawowe informacje'), {
            'fields': ('date', 'category', 'vendor', 'amount')
        }),
        (_('Szczegóły'), {
            'fields': ('description', 'notes')
        }),
        (_('Paragon'), {
            'fields': ('receipt_photo', 'receipt_preview')
        }),
        (_('Metadane'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def amount_display(self, obj):
        return format_html('<strong>{:.2f} PLN</strong>', obj.amount)
    amount_display.short_description = _('Kwota')
    amount_display.admin_order_field = 'amount'

    def description_short(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description
    description_short.short_description = _('Opis')

    def has_receipt(self, obj):
        if obj.receipt_photo:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_receipt.short_description = _('Paragon')

    def receipt_preview(self, obj):
        if obj.receipt_photo:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-width: 300px; max-height: 300px;" /></a>',
                obj.receipt_photo.url,
                obj.receipt_photo.url
            )
        return _('Brak zdjęcia')
    receipt_preview.short_description = _('Podgląd paragonu')


class RoomProgressPhotoInline(admin.TabularInline):
    model = RoomProgressPhoto
    extra = 1
    fields = ['photo', 'photo_preview', 'caption', 'uploaded_at']
    readonly_fields = ['photo_preview', 'uploaded_at']

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-width: 150px; max-height: 150px;" /></a>',
                obj.photo.url,
                obj.photo.url
            )
        return _('Brak zdjęcia')
    photo_preview.short_description = _('Podgląd')


class ElectricalCircuitInline(admin.TabularInline):
    model = ElectricalCircuit
    extra = 0
    fields = ['breaker_number', 'circuit_name', 'amperage', 'connected_appliances']
    show_change_link = True


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['get_name_display_custom', 'square_meters', 'get_progress_count', 'get_circuit_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'get_progress_count', 'get_circuit_count', 'get_work_sessions_count']
    inlines = [ElectricalCircuitInline]

    fieldsets = (
        (_('Podstawowe informacje'), {
            'fields': ('name', 'square_meters', 'description')
        }),
        (_('Statystyki'), {
            'fields': ('get_progress_count', 'get_circuit_count', 'get_work_sessions_count'),
            'classes': ('collapse',)
        }),
        (_('Metadane'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_name_display_custom(self, obj):
        return obj.get_name_display()
    get_name_display_custom.short_description = _('Pomieszczenie')
    get_name_display_custom.admin_order_field = 'name'

    def get_progress_count(self, obj):
        count = obj.progress_entries.count()
        url = reverse('admin:renovation_roomprogress_changelist') + f'?room__id__exact={obj.id}'
        return format_html('<a href="{}">{} wpisów</a>', url, count)
    get_progress_count.short_description = _('Postępy prac')

    def get_circuit_count(self, obj):
        count = obj.circuits.count()
        return format_html('<strong>{}</strong>', count)
    get_circuit_count.short_description = _('Obwody elektryczne')

    def get_work_sessions_count(self, obj):
        count = obj.work_sessions.count()
        return format_html('<strong>{}</strong>', count)
    get_work_sessions_count.short_description = _('Sesje pracy')


@admin.register(RoomProgress)
class RoomProgressAdmin(admin.ModelAdmin):
    list_display = ['room', 'date', 'description_short', 'get_photo_count', 'created_at']
    list_filter = ['room', 'date']
    search_fields = ['description', 'notes', 'room__name']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'get_photo_count']
    inlines = [RoomProgressPhotoInline]
    list_per_page = 50

    fieldsets = (
        (_('Podstawowe informacje'), {
            'fields': ('room', 'date')
        }),
        (_('Postęp prac'), {
            'fields': ('description', 'notes')
        }),
        (_('Statystyki'), {
            'fields': ('get_photo_count',),
            'classes': ('collapse',)
        }),
        (_('Metadane'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def description_short(self, obj):
        if len(obj.description) > 60:
            return obj.description[:60] + '...'
        return obj.description
    description_short.short_description = _('Opis')

    def get_photo_count(self, obj):
        count = obj.photos.count()
        return format_html('<strong>{} zdjęć</strong>', count)
    get_photo_count.short_description = _('Liczba zdjęć')


@admin.register(RoomProgressPhoto)
class RoomProgressPhotoAdmin(admin.ModelAdmin):
    list_display = ['get_thumbnail', 'progress', 'caption_short', 'uploaded_at']
    list_filter = ['progress__room', 'uploaded_at']
    search_fields = ['caption', 'progress__description']
    readonly_fields = ['uploaded_at', 'photo_preview']
    date_hierarchy = 'uploaded_at'
    list_per_page = 50

    fieldsets = (
        (_('Podstawowe informacje'), {
            'fields': ('progress', 'caption')
        }),
        (_('Zdjęcie'), {
            'fields': ('photo', 'photo_preview')
        }),
        (_('Metadane'), {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )

    def get_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover;" />',
                obj.photo.url
            )
        return _('Brak')
    get_thumbnail.short_description = _('Miniatura')

    def caption_short(self, obj):
        if obj.caption:
            if len(obj.caption) > 40:
                return obj.caption[:40] + '...'
            return obj.caption
        return _('(bez podpisu)')
    caption_short.short_description = _('Podpis')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-width: 500px; max-height: 500px;" /></a>',
                obj.photo.url,
                obj.photo.url
            )
        return _('Brak zdjęcia')
    photo_preview.short_description = _('Podgląd zdjęcia')


@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    list_display = ['date', 'start_time', 'end_time', 'get_duration', 'get_rooms_list', 'notes_short']
    list_filter = ['date', 'rooms_worked_on']
    search_fields = ['notes', 'rooms_worked_on__name']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'get_duration']
    filter_horizontal = ['rooms_worked_on']
    list_per_page = 50

    fieldsets = (
        (_('Czas'), {
            'fields': ('date', 'start_time', 'end_time', 'get_duration')
        }),
        (_('Szczegóły'), {
            'fields': ('notes', 'rooms_worked_on')
        }),
        (_('Metadane'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_duration(self, obj):
        duration = obj.duration
        if duration:
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            return format_html('<strong>{}h {}m</strong>', hours, minutes)
        return "-"
    get_duration.short_description = _('Czas trwania')

    def get_rooms_list(self, obj):
        rooms = obj.rooms_worked_on.all()
        if rooms:
            room_names = ', '.join([r.get_name_display() for r in rooms])
            return room_names
        return _('(brak)')
    get_rooms_list.short_description = _('Pomieszczenia')

    def notes_short(self, obj):
        if len(obj.notes) > 50:
            return obj.notes[:50] + '...'
        return obj.notes
    notes_short.short_description = _('Notatki')


@admin.register(ElectricalCircuit)
class ElectricalCircuitAdmin(admin.ModelAdmin):
    list_display = ['breaker_number', 'circuit_name', 'room', 'amperage_display', 'appliances_short']
    list_filter = ['room', 'amperage']
    search_fields = ['circuit_name', 'breaker_number', 'connected_appliances', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 50

    fieldsets = (
        (_('Podstawowe informacje'), {
            'fields': ('circuit_name', 'breaker_number', 'room', 'amperage')
        }),
        (_('Szczegóły'), {
            'fields': ('connected_appliances', 'notes')
        }),
        (_('Metadane'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def amperage_display(self, obj):
        if obj.amperage:
            return format_html('<strong>{}A</strong>', obj.amperage)
        return _('(nie określono)')
    amperage_display.short_description = _('Amperaż')
    amperage_display.admin_order_field = 'amperage'

    def appliances_short(self, obj):
        if len(obj.connected_appliances) > 50:
            return obj.connected_appliances[:50] + '...'
        return obj.connected_appliances
    appliances_short.short_description = _('Urządzenia')
