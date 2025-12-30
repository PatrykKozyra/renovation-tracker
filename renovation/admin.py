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


# Purchase admin removed - use custom form at /purchases/add/ instead
# @admin.register(Purchase)
# class PurchaseAdmin(admin.ModelAdmin):
#     ... (admin interface disabled to encourage use of modern UI)


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


# RoomProgress admin removed - use custom form at /progress/add/ instead
# @admin.register(RoomProgress)
# class RoomProgressAdmin(admin.ModelAdmin):
#     ... (admin interface disabled to encourage use of modern UI)


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


# WorkSession admin removed - use custom form at /sessions/add/ instead
# @admin.register(WorkSession)
# class WorkSessionAdmin(admin.ModelAdmin):
#     ... (admin interface disabled to encourage use of modern UI)


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
