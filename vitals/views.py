from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from vitals.models import Vital

# Create your views here.
class VitalIndexView(ListView, LoginRequiredMixin):
    paginate_by = 10

    def get_queryset(self):

        user = self.request.user

        vitals = Vital.objects.filter(user=user).order_by("-created").all()

        return vitals
    
class VitalCreateView(CreateView, LoginRequiredMixin):
    success_url = reverse_lazy('vitals:index')
    model = Vital
    fields = ['date', 'type', 'value']
    template_name = "vitals/create.html"

    def form_valid(self, form):
        
        form.instance.user = self.request.user

        return super().form_valid(form)