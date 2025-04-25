from django.urls import path

from . import views

app_name = 'vitals'


urlpatterns = [
    path('', views.VitalIndexView.as_view(), name='index'),
    path('create/', views.VitalCreateView.as_view(), name='create'),
    path('blood/', views.BloodCreateView.as_view(), name='blood'),
    path('update/<int:pk>/', views.VitalUpdateView.as_view(), name='update')
]