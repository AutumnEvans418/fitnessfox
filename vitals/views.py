from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from vitals.models import Vital

# Create your views here.
class VitalIndexView(ListView, LoginRequiredMixin):
    paginate_by = 10

    def get_queryset(self):

        user = self.request.user

        vitals = Vital.objects.filter(user=user).order_by("-created").all()

        return vitals