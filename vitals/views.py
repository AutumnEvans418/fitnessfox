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

from collections import defaultdict
from typing import Callable, Iterable, TypeVar, Dict, List

import jsonpickle

from .forms import BloodForm

T = TypeVar('T')
K = TypeVar('K')

def group_by(items: Iterable[T], key_func: Callable[[T], K]) -> Dict[K, List[T]]:
    grouped = defaultdict(list)
    for item in items:
        grouped[key_func(item)].append(item)
    return dict(grouped)

class VitalChartData:
    def __init__(self, date: str, type: str, type_id: int, value: int):
        self.date = date
        self.type = type
        self.type_id = type_id
        self.value = value
        pass

# Create your views here.
class VitalIndexView(ListView, LoginRequiredMixin):
    paginate_by = 5

    def get_queryset(self):

        user = self.request.user

        vitals = Vital.objects.filter(user=user).order_by("-date").all()

        return vitals
    
    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        user = self.request.user

        data = [ VitalChartData(
            str(r.date)[0:10],
            r.get_type_display(),
            r.type,
            r.value) for r in Vital.objects.filter(user=user).order_by("-date").all()] 

        def getGeneralData(data, type, title):
            data = sorted([x for x in data if x.type_id == type], key=lambda p: p.date)

            date_data = list(group_by(data, lambda x: x.date).values())
            labels = [x[0].date for x in date_data]

            result = []
            for label in labels:
                values = [x.value for x in data if x.date == label]
                if values:
                    value = sum(values)/len(values)
                    result.append(value)
                else:
                    result.append(None)
            
            return {
                "text": title,
                "type": "line",
                "min": 0,
                "max": 150,
                "labels": labels,
                "data": [
                    {
                        "label": title,
                        "data": result,
                        "color": "#23b5d3",                      
                    }
                ]
            }



        def getHeartData(data):
            data = sorted([x for x in data if x.type_id in [Vital.BPM, Vital.DIASTOLIC, Vital.SYSTOLIC]], key=lambda p: p.date)

            date_data = list(group_by(data, lambda x: x.date).values())

            labels = [x[0].date for x in date_data]

            bpm = []
            diastolic = []
            systolic = []

            for label in labels:

                def addList(type, d):
                    values = [x.value for x in data if x.date == label and x.type_id == type]
                    if values:
                        value = sum(values)/len(values)
                        d.append(value)
                    else:
                        d.append(None)
                
                addList(Vital.BPM, bpm)
                addList(Vital.DIASTOLIC, diastolic)
                addList(Vital.SYSTOLIC, systolic)

            return {
                "text": "Heart Vitals",
                "type": "line",
                "min": 0,
                "max": 150,
                "labels": labels,
                "data": [
                    {
                        "label": "Bpm",
                        "data": bpm,
                        "color": "#23b5d3",                      
                    },
                    {
                        "label": "Systolic",
                        "data": systolic,
                        "color": "#279af1",                    
                    },
                    {
                        "label": "Diastolic",
                        "data": diastolic,
                        "color": "#ea526f",                       
                    }
                ]
            }

        charts = [
            getHeartData(data),
            getGeneralData(data, Vital.WEIGHT, "Weight"),
            getGeneralData(data, Vital.TEMPERATURE, "Temperature")
        ]

        ctx['object_list_json'] = jsonpickle.encode(data)

        ctx['charts'] = [{
            "name": chart['text'], 
            'data': jsonpickle.encode(chart)} for chart in charts] 

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
    
class BloodCreateView(FormView):
    form_class = BloodForm
    success_url = reverse_lazy('vitals:index')
    template_name = "vitals/create.html"

    def form_valid(self, form):

        user = self.request.user

        valid = super().form_valid(form)

        form.save(user)

        return valid