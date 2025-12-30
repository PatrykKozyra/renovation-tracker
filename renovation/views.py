from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from datetime import timedelta, datetime, date
from calendar import monthrange
import json
from .models import Purchase, RoomProgress, RoomProgressPhoto, WorkSession, PurchaseCategory, Room, ElectricalCircuit, Property, DropdownChoice, Equipment, EquipmentPhoto, EquipmentAssignment
from .forms import PurchaseForm, RoomProgressForm, WorkSessionForm, ElectricalCircuitForm, PropertyForm, RoomForm, DropdownChoiceForm, EquipmentForm, EquipmentPhotoForm, EquipmentAssignmentForm


def get_current_property(request):
    """Get the current property from session or user's first property"""
    property_id = request.session.get('current_property_id')

    if property_id:
        try:
            return Property.objects.get(id=property_id, owner=request.user)
        except Property.DoesNotExist:
            pass

    # Get user's first active property
    property_obj = Property.objects.filter(owner=request.user, is_active=True).first()
    if property_obj:
        request.session['current_property_id'] = property_obj.id
    return property_obj


@login_required
def dashboard(request):
    """Comprehensive dashboard with analytics"""

    # Get current property
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    # Total spending (for current property)
    total_spent = Purchase.objects.filter(property=current_property).aggregate(Sum('amount'))['amount__sum'] or 0
    purchase_count = Purchase.objects.filter(property=current_property).count()

    # Recent purchases (last 10) from current property
    recent_purchases = Purchase.objects.filter(property=current_property).select_related('category').order_by('-date')[:10]

    # Progress entries from current property
    progress_entries_count = RoomProgress.objects.filter(room__property=current_property).count()
    recent_progress = RoomProgress.objects.filter(room__property=current_property).select_related('room').prefetch_related('photos').order_by('-date')[:5]

    # Work sessions - This month vs Total
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)

    # Total hours
    all_sessions = WorkSession.objects.all()
    total_duration = timedelta()
    for session in all_sessions:
        if session.duration:
            total_duration += session.duration
    total_work_hours = total_duration.total_seconds() / 3600

    # This month hours
    this_month_sessions = WorkSession.objects.filter(date__gte=first_day_of_month)
    month_duration = timedelta()
    for session in this_month_sessions:
        if session.duration:
            month_duration += session.duration
    month_work_hours = month_duration.total_seconds() / 3600

    work_sessions_count = all_sessions.count()
    month_sessions_count = this_month_sessions.count()

    # Photos
    total_photos = RoomProgressPhoto.objects.count()

    # Category spending for pie chart
    categories = PurchaseCategory.objects.annotate(
        total=Sum('purchases__amount'),
        count=Count('purchases')
    ).filter(total__isnull=False).order_by('-total')

    category_labels = []
    category_data = []
    category_colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF', '#4BC0C0']

    for idx, cat in enumerate(categories):
        category_labels.append(cat.get_name_display())
        category_data.append(float(cat.total))

    # Monthly spending trends (last 6 months)
    six_months_ago = today - timedelta(days=180)
    monthly_data = Purchase.objects.filter(
        date__gte=six_months_ago
    ).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('month')

    monthly_labels = []
    monthly_amounts = []
    for item in monthly_data:
        month_name = item['month'].strftime('%b %Y')
        monthly_labels.append(month_name)
        monthly_amounts.append(float(item['total']))

    # Room progress status
    all_rooms = Room.objects.all()
    room_status = []
    for room in all_rooms:
        latest_progress = room.progress_entries.order_by('-date').first()
        progress_count = room.progress_entries.count()

        # Calculate progress percentage (based on number of updates)
        # You can customize this logic
        max_expected_updates = 10  # Assume 10 updates means 100%
        progress_percentage = min(100, (progress_count / max_expected_updates) * 100)

        latest_photo = None
        if latest_progress:
            latest_photo_obj = latest_progress.photos.first()
            if latest_photo_obj:
                latest_photo = latest_photo_obj.photo.url

        room_status.append({
            'room': room,
            'name': room.get_name_display(),
            'progress_count': progress_count,
            'progress_percentage': int(progress_percentage),
            'latest_progress': latest_progress,
            'latest_photo': latest_photo,
        })

    # Top vendors by spending
    from django.db.models import Sum as DbSum
    top_vendors = Purchase.objects.values('vendor').annotate(
        total=DbSum('amount'),
        count=Count('id')
    ).order_by('-total')[:5]

    context = {
        'current_property': current_property,
        'total_spent': total_spent,
        'purchase_count': purchase_count,
        'recent_purchases': recent_purchases,
        'progress_entries_count': progress_entries_count,
        'recent_progress': recent_progress,
        'work_sessions_count': work_sessions_count,
        'month_sessions_count': month_sessions_count,
        'total_work_hours': total_work_hours,
        'month_work_hours': month_work_hours,
        'total_photos': total_photos,
        'room_status': room_status,
        'top_vendors': top_vendors,
        # Chart data
        'category_labels_json': json.dumps(category_labels),
        'category_data_json': json.dumps(category_data),
        'category_colors_json': json.dumps(category_colors[:len(category_labels)]),
        'monthly_labels_json': json.dumps(monthly_labels),
        'monthly_amounts_json': json.dumps(monthly_amounts),
    }

    return render(request, 'renovation/dashboard.html', context)


def user_login(request):
    """Login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            messages.success(request, _('Zalogowano pomyślnie!'))
            return redirect(next_url)
        else:
            messages.error(request, _('Nieprawidłowa nazwa użytkownika lub hasło.'))

    return render(request, 'renovation/login.html')


def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, _('Wylogowano pomyślnie.'))
    return redirect('login')


@login_required
def purchases_list(request):
    """List all purchases"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    purchases = Purchase.objects.filter(property=current_property).select_related('category').order_by('-date')

    context = {
        'current_property': current_property,
        'purchases': purchases,
        'total_spent': purchases.aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    return render(request, 'renovation/purchases_list.html', context)


@login_required
def progress_list(request):
    """List all progress entries"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    progress_entries = RoomProgress.objects.filter(
        room__property=current_property
    ).select_related('room').prefetch_related('photos').order_by('-date')

    context = {
        'current_property': current_property,
        'progress_entries': progress_entries,
    }

    return render(request, 'renovation/progress_list.html', context)


@login_required
def sessions_list(request):
    """List all work sessions"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    # Filter sessions by rooms that belong to current property
    sessions = WorkSession.objects.filter(
        rooms_worked_on__property=current_property
    ).distinct().prefetch_related('rooms_worked_on').order_by('-date', '-start_time')

    # Calculate total hours
    total_duration = timedelta()
    for session in sessions:
        if session.duration:
            total_duration += session.duration
    total_hours = total_duration.total_seconds() / 3600

    context = {
        'current_property': current_property,
        'sessions': sessions,
        'total_hours': total_hours,
    }

    return render(request, 'renovation/sessions_list.html', context)


@login_required
def purchase_add(request):
    """Add a new purchase with beautiful form"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.property = current_property
            purchase.save()
            messages.success(request, _('Zakup został dodany pomyślnie!'))
            return redirect('purchases_list')
    else:
        form = PurchaseForm()

    context = {
        'current_property': current_property,
        'form': form,
        'title': _('Dodaj zakup'),
        'action_url': 'purchase_add',
    }
    return render(request, 'renovation/purchase_form.html', context)


@login_required
def purchase_edit(request, pk):
    """Edit an existing purchase"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    purchase = get_object_or_404(Purchase, pk=pk, property=current_property)

    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES, instance=purchase)
        if form.is_valid():
            form.save()
            messages.success(request, _('Zakup został zaktualizowany!'))
            return redirect('purchases_list')
    else:
        form = PurchaseForm(instance=purchase)

    context = {
        'current_property': current_property,
        'form': form,
        'title': _('Edytuj zakup'),
        'action_url': 'purchase_edit',
        'purchase': purchase,
    }
    return render(request, 'renovation/purchase_form.html', context)


@login_required
def progress_add(request):
    """Add a new room progress entry with photos"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    if request.method == 'POST':
        form = RoomProgressForm(request.POST, current_property=current_property)
        photos = request.FILES.getlist('photos')

        if form.is_valid():
            progress = form.save()

            # Save all uploaded photos
            for photo in photos:
                RoomProgressPhoto.objects.create(progress=progress, photo=photo)

            messages.success(request, _('Postęp został dodany pomyślnie!'))
            return redirect('progress_list')
    else:
        form = RoomProgressForm(current_property=current_property)

    context = {
        'form': form,
        'title': _('Dodaj postęp'),
    }
    return render(request, 'renovation/progress_form.html', context)


@login_required
def session_add(request):
    """Add a new work session"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    if request.method == 'POST':
        form = WorkSessionForm(request.POST, current_property=current_property)
        if form.is_valid():
            form.save()
            messages.success(request, _('Sesja została dodana pomyślnie!'))
            return redirect('sessions_list')
    else:
        form = WorkSessionForm(current_property=current_property)

    context = {
        'current_property': current_property,
        'form': form,
        'title': _('Dodaj sesję pracy'),
    }
    return render(request, 'renovation/session_form.html', context)


@login_required
def circuit_add(request):
    """Add a new electrical circuit"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    if request.method == 'POST':
        form = ElectricalCircuitForm(request.POST, current_property=current_property)
        if form.is_valid():
            form.save()
            messages.success(request, _('Obwód elektryczny został dodany!'))
            return redirect('dashboard')
    else:
        form = ElectricalCircuitForm(current_property=current_property)

    context = {
        'form': form,
        'title': _('Dodaj obwód elektryczny'),
    }
    return render(request, 'renovation/circuit_form.html', context)


# Property Management Views

@login_required
def property_list(request):
    """List all properties for current user"""
    properties = Property.objects.filter(owner=request.user).order_by('-is_active', '-created_at')
    current_property = get_current_property(request)

    context = {
        'properties': properties,
        'current_property': current_property,
    }
    return render(request, 'renovation/property_list.html', context)


@login_required
def property_add(request):
    """Add a new property"""
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()

            # Set as current property
            request.session['current_property_id'] = property_obj.id

            messages.success(request, _('Nieruchomość została dodana pomyślnie!'))
            return redirect('dashboard')
    else:
        form = PropertyForm()

    context = {
        'form': form,
        'title': _('Dodaj nieruchomość'),
    }
    return render(request, 'renovation/property_form.html', context)


@login_required
def property_edit(request, pk):
    """Edit an existing property"""
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, _('Nieruchomość została zaktualizowana!'))
            return redirect('property_list')
    else:
        form = PropertyForm(instance=property_obj)

    context = {
        'form': form,
        'title': _('Edytuj nieruchomość'),
        'property': property_obj,
    }
    return render(request, 'renovation/property_form.html', context)


@login_required
def property_switch(request, pk):
    """Switch to a different property"""
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    request.session['current_property_id'] = property_obj.id
    messages.success(request, _('Przełączono na nieruchomość: {}').format(property_obj.name))
    return redirect('dashboard')


# Room Management Views

@login_required
def room_list(request):
    """List all rooms for current property"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    rooms = Room.objects.filter(property=current_property).order_by('name')

    context = {
        'current_property': current_property,
        'rooms': rooms,
    }
    return render(request, 'renovation/room_list.html', context)


@login_required
def room_add(request):
    """Add a new room to current property"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.property = current_property
            room.save()
            messages.success(request, _('Pomieszczenie zostało dodane pomyślnie!'))
            return redirect('room_list')
    else:
        form = RoomForm()

    context = {
        'current_property': current_property,
        'form': form,
        'title': _('Dodaj pomieszczenie'),
    }
    return render(request, 'renovation/room_form.html', context)


@login_required
def room_edit(request, pk):
    """Edit an existing room"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    room = get_object_or_404(Room, pk=pk, property=current_property)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, _('Pomieszczenie zostało zaktualizowane!'))
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)

    context = {
        'current_property': current_property,
        'form': form,
        'title': _('Edytuj pomieszczenie'),
        'room': room,
    }
    return render(request, 'renovation/room_form.html', context)


@login_required
def room_detail(request, pk):
    """View room details"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    room = get_object_or_404(Room, pk=pk, property=current_property)

    # Get wall finishes as list
    wall_finishes_list = []
    if room.wall_finishes:
        wall_finishes_list = [finish.strip() for finish in room.wall_finishes.split(',')]

    context = {
        'current_property': current_property,
        'room': room,
        'wall_finishes_list': wall_finishes_list,
    }
    return render(request, 'renovation/room_detail.html', context)


# ========================================
# Dropdown Management Views
# ========================================

@login_required
def dropdown_mapping_list(request):
    """List all dropdown choices grouped by type"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    # Group dropdown choices by type
    choices_by_type = {}
    for choice_type, choice_label in DropdownChoice.CHOICE_TYPE_CHOICES:
        choices_by_type[choice_type] = {
            'label': choice_label,
            'choices': DropdownChoice.objects.filter(choice_type=choice_type).order_by('display_order', 'label_pl')
        }

    context = {
        'current_property': current_property,
        'choices_by_type': choices_by_type,
        'choice_types': DropdownChoice.CHOICE_TYPE_CHOICES,
    }
    return render(request, 'renovation/dropdown_mapping_list.html', context)


@login_required
def dropdown_choice_add(request):
    """Add a new dropdown choice"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    if request.method == 'POST':
        form = DropdownChoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Opcja została dodana pomyślnie.'))
            return redirect('dropdown_mapping_list')
    else:
        form = DropdownChoiceForm()

    context = {
        'current_property': current_property,
        'form': form,
        'title': _('Dodaj opcję'),
    }
    return render(request, 'renovation/dropdown_choice_form.html', context)


@login_required
def dropdown_choice_edit(request, pk):
    """Edit an existing dropdown choice"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    choice = get_object_or_404(DropdownChoice, pk=pk)

    if request.method == 'POST':
        form = DropdownChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            messages.success(request, _('Opcja została zaktualizowana.'))
            return redirect('dropdown_mapping_list')
    else:
        form = DropdownChoiceForm(instance=choice)

    context = {
        'current_property': current_property,
        'form': form,
        'title': _('Edytuj opcję'),
        'choice': choice,
    }
    return render(request, 'renovation/dropdown_choice_form.html', context)


@login_required
def dropdown_choice_delete(request, pk):
    """Delete a dropdown choice"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    choice = get_object_or_404(DropdownChoice, pk=pk)

    if request.method == 'POST':
        choice.delete()
        messages.success(request, _('Opcja została usunięta.'))
        return redirect('dropdown_mapping_list')

    context = {
        'current_property': current_property,
        'choice': choice,
    }
    return render(request, 'renovation/dropdown_choice_confirm_delete.html', context)


# ========================================
# Equipment Management Views
# ========================================

@login_required
def equipment_list(request):
    """List all equipment for the current user"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    # Get all equipment for current user
    equipment_items = Equipment.objects.filter(owner=request.user).prefetch_related('photos', 'assignments')

    context = {
        'current_property': current_property,
        'equipment_items': equipment_items,
    }
    return render(request, 'renovation/equipment_list.html', context)


@login_required
def equipment_add(request):
    """Add new equipment"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.owner = request.user
            equipment.save()
            messages.success(request, _('Sprzęt został dodany pomyślnie.'))
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm()

    context = {
        'current_property': current_property,
        'form': form,
        'title': _('Dodaj narzędzie/sprzęt'),
    }
    return render(request, 'renovation/equipment_form.html', context)


@login_required
def equipment_detail(request, pk):
    """View equipment details with photos and assignment history"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    equipment = get_object_or_404(Equipment, pk=pk, owner=request.user)
    photos = equipment.photos.all()
    assignments = equipment.assignments.all()

    context = {
        'current_property': current_property,
        'equipment': equipment,
        'photos': photos,
        'assignments': assignments,
        'can_add_photo': photos.count() < 5,
    }
    return render(request, 'renovation/equipment_detail.html', context)


@login_required
def equipment_edit(request, pk):
    """Edit existing equipment"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    equipment = get_object_or_404(Equipment, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, _('Sprzęt został zaktualizowany.'))
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm(instance=equipment)

    context = {
        'current_property': current_property,
        'form': form,
        'title': _('Edytuj sprzęt'),
        'equipment': equipment,
    }
    return render(request, 'renovation/equipment_form.html', context)


@login_required
def equipment_delete(request, pk):
    """Delete equipment"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    equipment = get_object_or_404(Equipment, pk=pk, owner=request.user)

    if request.method == 'POST':
        equipment.delete()
        messages.success(request, _('Sprzęt został usunięty.'))
        return redirect('equipment_list')

    context = {
        'current_property': current_property,
        'equipment': equipment,
    }
    return render(request, 'renovation/equipment_confirm_delete.html', context)


@login_required
def equipment_photo_add(request, equipment_pk):
    """Add photo to equipment"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    equipment = get_object_or_404(Equipment, pk=equipment_pk, owner=request.user)

    # Check if max photos reached
    if equipment.photos.count() >= 5:
        messages.error(request, _('Maksymalna liczba zdjęć (5) została osiągnięta.'))
        return redirect('equipment_detail', pk=equipment.pk)

    if request.method == 'POST':
        form = EquipmentPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.equipment = equipment
            photo.save()
            messages.success(request, _('Zdjęcie zostało dodane.'))
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentPhotoForm()

    context = {
        'current_property': current_property,
        'form': form,
        'equipment': equipment,
        'title': _('Dodaj zdjęcie sprzętu'),
    }
    return render(request, 'renovation/equipment_photo_form.html', context)


@login_required
def equipment_photo_delete(request, pk):
    """Delete equipment photo"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    photo = get_object_or_404(EquipmentPhoto, pk=pk, equipment__owner=request.user)
    equipment = photo.equipment

    if request.method == 'POST':
        photo.delete()
        messages.success(request, _('Zdjęcie zostało usunięte.'))
        return redirect('equipment_detail', pk=equipment.pk)

    context = {
        'current_property': current_property,
        'photo': photo,
        'equipment': equipment,
    }
    return render(request, 'renovation/equipment_photo_confirm_delete.html', context)


@login_required
def equipment_assign(request, equipment_pk):
    """Assign equipment to a property"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    equipment = get_object_or_404(Equipment, pk=equipment_pk, owner=request.user)

    # Check if equipment is sold
    if equipment.is_sold:
        messages.error(request, _('Nie można przypisać sprzedanego sprzętu do nieruchomości.'))
        return redirect('equipment_detail', pk=equipment.pk)

    # Check if already assigned
    if equipment.is_assigned:
        messages.error(request, _('Sprzęt jest już przypisany do nieruchomości. Zwolnij go najpierw.'))
        return redirect('equipment_detail', pk=equipment.pk)

    if request.method == 'POST':
        form = EquipmentAssignmentForm(request.POST, user=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.equipment = equipment
            assignment.save()
            messages.success(request, _('Sprzęt został przypisany do nieruchomości.'))
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentAssignmentForm(user=request.user, initial={'start_date': date.today()})

    context = {
        'current_property': current_property,
        'form': form,
        'equipment': equipment,
        'title': _('Przypisz sprzęt do nieruchomości'),
    }
    return render(request, 'renovation/equipment_assign_form.html', context)


@login_required
def equipment_unassign(request, equipment_pk):
    """Free equipment from property assignment"""
    current_property = get_current_property(request)
    if not current_property:
        messages.warning(request, _('Proszę dodać nieruchomość przed rozpoczęciem pracy.'))
        return redirect('property_add')

    equipment = get_object_or_404(Equipment, pk=equipment_pk, owner=request.user)
    assignment = equipment.current_assignment

    if not assignment:
        messages.error(request, _('Sprzęt nie jest obecnie przypisany do żadnej nieruchomości.'))
        return redirect('equipment_detail', pk=equipment.pk)

    if request.method == 'POST':
        assignment.end_date = date.today()
        assignment.save()
        messages.success(request, _('Sprzęt został zwolniony z nieruchomości.'))
        return redirect('equipment_detail', pk=equipment.pk)

    context = {
        'current_property': current_property,
        'equipment': equipment,
        'assignment': assignment,
    }
    return render(request, 'renovation/equipment_unassign_confirm.html', context)
