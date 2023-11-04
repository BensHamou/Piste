import django_filters
from django_filters import FilterSet
from django import forms
from .forms import getAttrs
from .models import *
from django.db.models import Q

class PisteFilter(FilterSet):

    search = django_filters.CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher..')))

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(object__icontains=value) |
            Q(client__icontains=value)
        ).distinct()

    class Meta:
        model = Piste
        fields = ['search']