from gamble.views import AutoCreatePatternSlotsView, GetTheRandomBoxView

from django.urls import path

urlpatterns = [
    path('spin/<int:slot_machine_id>/', GetTheRandomBoxView.as_view()),
    path('auto-complete/', AutoCreatePatternSlotsView.as_view())
]