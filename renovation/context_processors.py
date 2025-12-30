from django.db.models import Sum, Count
from datetime import timedelta
from .models import Purchase, RoomProgress, RoomProgressPhoto, WorkSession, PurchaseCategory, Room


def admin_dashboard_stats(request):
    """Context processor for admin dashboard statistics"""

    if not request.path.startswith('/admin/'):
        return {}

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

    return {
        'total_spent': total_spent,
        'purchase_count': purchase_count,
        'progress_entries_count': progress_entries_count,
        'work_sessions_count': work_sessions_count,
        'total_work_hours': total_work_hours,
        'total_photos': total_photos,
        'category_spending': category_spending,
        'room_progress': room_progress,
    }
