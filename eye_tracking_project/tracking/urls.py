
# tracking/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('eye_tracking_data/', views.EyeTrackingDataView.as_view(), name='eye_tracking_data'),
]
