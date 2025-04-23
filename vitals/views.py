from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from vitals.models import Vital

from rest_framework.views import APIView 
from rest_framework.response import Response 
from json import dumps 
from django.core import serializers

# Create your views here.
class VitalIndexView(ListView, LoginRequiredMixin):
    paginate_by = 10

    def get_queryset(self):

        user = self.request.user

        vitals = Vital.objects.filter(user=user).order_by("-created").all()

        return vitals
    
    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        list = ctx['object_list']

        data = serializers.serialize('json', list)

        ctx['object_list_json'] = data

        mapper = dumps(Vital.VITAL_CHOICES)

        ctx['vital_types'] = mapper

        return ctx
    
class VitalCreateView(CreateView, LoginRequiredMixin):
    success_url = reverse_lazy('vitals:index')
    model = Vital
    fields = ['date', 'type', 'value']
    template_name = "vitals/create.html"

    def form_valid(self, form):
        
        form.instance.user = self.request.user

        return super().form_valid(form)