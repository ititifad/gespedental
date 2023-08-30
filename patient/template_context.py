from datetime import datetime, timedelta
from .models import MedicalHistory

def upcoming_follow_up_count(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    upcoming_follow_up_count = MedicalHistory.objects.filter(follow_up_date=tomorrow).count()
    return {'upcoming_follow_up_count': upcoming_follow_up_count}
