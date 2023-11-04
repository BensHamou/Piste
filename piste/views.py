from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import uuid
from .forms import *
from .filters import *
from django.core.paginator import Paginator
from django.urls import reverse

@login_required(login_url='login')
def listPisteList(request):
    pistes = Piste.objects.all().order_by('id')
    filteredData = PisteFilter(request.GET, queryset=pistes)
    pistes = filteredData.qs
    paginator = Paginator(pistes, 7)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page, 'filtredData': filteredData, 
    }
    return render(request, 'list_pistes.html', context)

@login_required(login_url='login')
def deletePisteView(request, id):
    piste = Piste.objects.get(id=id)
    piste.delete()
    cache_param = str(uuid.uuid4())
    url_path = reverse('pistes')

    redirect_url = f'{url_path}?cache={cache_param}'

    return redirect(redirect_url)

@login_required(login_url='login')
def createPisteView(request):
    form = PisteForm()
    if request.method == 'POST':
        form = PisteForm(request.POST)
        if form.is_valid():
            form.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('pistes')
            redirect_url = f'{url_path}?cache={cache_param}'
            return redirect(redirect_url)
    context = {'form': form }
    return render(request, 'piste_form.html', context)

@login_required(login_url='login')
def editPisteView(request, id):
    piste = Piste.objects.get(id=id)

    form = PisteForm(instance=piste)
    if request.method == 'POST':
        form = PisteForm(request.POST, instance=piste )
        if form.is_valid():
            form.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('pistes')
            page = request.GET.get('page', '1')
            redirect_url = f'{url_path}?cache={cache_param}&page={page}'
            return redirect(redirect_url)
    context = {'form': form, 'piste': piste }

    return render(request, 'piste_form.html', context)

