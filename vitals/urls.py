from django.urls import path

from . import views

urlpatterns = [
    path('', views.VitalIndexView.as_view())
]