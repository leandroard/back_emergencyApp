from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Emergency

@shared_task
def update_emergency_status():
    ten_minutes_ago = timezone.now() - timedelta(minutes=2)
    Emergency.objects.filter(status='active', created_at__lte=ten_minutes_ago).update(status='inactive')
