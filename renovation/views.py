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
from .models import Purchase, RoomProgress, RoomProgressPhoto, WorkSession, PurchaseCategory, Room, ElectricalCircuit
from .forms import PurchaseForm, RoomProgressForm, WorkSessionForm, ElectricalCircuitForm


@login_required
def dashboard(request):
    """Comprehensive dashboard with analytics"""

    # Total spending
    total_spent = Purchase.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    purchase_count = Purchase.objects.count()

    # Recent purchases (last 10)
    recent_purchases = Purchase.objects.select_related('category').order_by('-date')[:10]

    # Progress entries
    progress_entries_count = RoomProgress.objects.count()
    recent_progress = RoomProgress.objects.select_related('room').prefetch_related('photos').order_by('-date')[:5]

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
    purchases = Purchase.objects.select_related('category').order_by('-date')

    context = {
        'purchases': purchases,
        'total_spent': purchases.aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    return render(request, 'renovation/purchases_list.html', context)


@login_required
def progress_list(request):
    """List all progress entries"""
    progress_entries = RoomProgress.objects.select_related('room').prefetch_related('photos').order_by('-date')

    context = {
        'progress_entries': progress_entries,
    }

    return render(request, 'renovation/progress_list.html', context)


@login_required
def sessions_list(request):
    """List all work sessions"""
    sessions = WorkSession.objects.prefetch_related('rooms_worked_on').order_by('-date', '-start_time')

    # Calculate total hours
    total_duration = timedelta()
    for session in sessions:
        if session.duration:
            total_duration += session.duration
    total_hours = total_duration.total_seconds() / 3600

    context = {
        'sessions': sessions,
        'total_hours': total_hours,
    }

    return render(request, 'renovation/sessions_list.html', context)


@login_required
def purchase_add(request):
    """Add a new purchase with beautiful form"""
    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('Zakup został dodany pomyślnie!'))
            return redirect('purchases_list')
    else:
        form = PurchaseForm()

    context = {
        'form': form,
        'title': _('Dodaj zakup'),
        'action_url': 'purchase_add',
    }
    return render(request, 'renovation/purchase_form.html', context)


@login_required
def purchase_edit(request, pk):
    """Edit an existing purchase"""
    purchase = get_object_or_404(Purchase, pk=pk)

    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES, instance=purchase)
        if form.is_valid():
            form.save()
            messages.success(request, _('Zakup został zaktualizowany!'))
            return redirect('purchases_list')
    else:
        form = PurchaseForm(instance=purchase)

    context = {
        'form': form,
        'title': _('Edytuj zakup'),
        'action_url': 'purchase_edit',
        'purchase': purchase,
    }
    return render(request, 'renovation/purchase_form.html', context)


@login_required
def progress_add(request):
    """Add a new room progress entry with photos"""
    if request.method == 'POST':
        form = RoomProgressForm(request.POST)
        photos = request.FILES.getlist('photos')

        if form.is_valid():
            progress = form.save()

            # Save all uploaded photos
            for photo in photos:
                RoomProgressPhoto.objects.create(progress=progress, photo=photo)

            messages.success(request, _('Postęp został dodany pomyślnie!'))
            return redirect('progress_list')
    else:
        form = RoomProgressForm()

    context = {
        'form': form,
        'title': _('Dodaj postęp'),
    }
    return render(request, 'renovation/progress_form.html', context)


@login_required
def session_add(request):
    """Add a new work session"""
    if request.method == 'POST':
        form = WorkSessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Sesja została dodana pomyślnie!'))
            return redirect('sessions_list')
    else:
        form = WorkSessionForm()

    context = {
        'form': form,
        'title': _('Dodaj sesję pracy'),
    }
    return render(request, 'renovation/session_form.html', context)


@login_required
def circuit_add(request):
    """Add a new electrical circuit"""
    if request.method == 'POST':
        form = ElectricalCircuitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Obwód elektryczny został dodany!'))
            return redirect('dashboard')
    else:
        form = ElectricalCircuitForm()

    context = {
        'form': form,
        'title': _('Dodaj obwód elektryczny'),
    }
    return render(request, 'renovation/circuit_form.html', context)
