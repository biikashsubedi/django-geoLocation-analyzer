from django.urls import path
from .views import distance_calculate_view

urlpatterns = [
    path('', distance_calculate_view, name='calculate-distance'),
]
