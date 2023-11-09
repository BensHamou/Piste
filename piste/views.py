from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import uuid
from .forms import *
from .filters import *
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import JsonResponse
from xmlrpc import client
from django.contrib import messages
from .cron import sync_with_odoo

def admin_only_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html', status=403)
    return wrapper

url = "http://10.20.10.43:8069"
#url = "http://10.23.10.101:8014"
db = 'hasnaoui'
username = "admin"
password = "28lWcgk9Np3D"

common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

@login_required(login_url='users:login')
def listPisteList(request):
    if request.user.is_admin:
        pistes = Piste.objects.all().order_by('-created_at')
    else:
        pistes = Piste.objects.filter(creator=request.user).order_by('id')
    filteredData = PisteFilter(request.GET, queryset=pistes)
    page_size_param = request.GET.get('page_size')
    page_size = int(page_size_param) if page_size_param else 12  
    pistes = filteredData.qs
    paginator = Paginator(pistes, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page, 'filtredData': filteredData, 
    }
    return render(request, 'list_pistes.html', context)

@login_required(login_url='users:login')
def deletePisteView(request, id):
    piste = Piste.objects.get(id=id)
    piste.delete()
    cache_param = str(uuid.uuid4())
    url_path = reverse('pistes')

    redirect_url = f'{url_path}?cache={cache_param}'

    return redirect(redirect_url)

@login_required(login_url='users:login')
def createPisteView(request):
    form = PisteForm()
    if request.method == 'POST':
        form = PisteForm(request.POST)
        if form.is_valid():
            piste = form.save(commit=False)
            piste.state = 'Brouillon'
            piste.creator = request.user
            piste.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('pistes')
            redirect_url = f'{url_path}?cache={cache_param}'
            return redirect(redirect_url)
    context = {'form': form }
    return render(request, 'piste_form.html', context)

@login_required(login_url='users:login')
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

@login_required(login_url='users:login')
def pisteDetailsView(request, id):
  piste = Piste.objects.get(id=id)
  context = {
    'piste_details': piste,
  }
  return render(request, 'piste_details.html', context)

@login_required(login_url='users:login')
def cancelPiste(request, pk):
    try:
        piste = Piste.objects.get(id=pk)
    except Piste.DoesNotExist:
        messages.success(request, 'Piste Does not exit')
        
    piste.state = 'Annulé'
    piste.save()
    url_path = reverse('detail_piste', args=[piste.id])
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)

@login_required(login_url='users:login')
def confirmPiste(request, pk):
    try:
        piste = Piste.objects.get(id=pk)
    except Piste.DoesNotExist:
        messages.success(request, 'Piste Does not exit')
    
    piste.state = 'Confirmé'
    piste.save()

    url_path = reverse('detail_piste', args=[piste.id])
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)

@login_required(login_url='users:login')
def live_search(request):

    search_for = request.GET.get('search_for', '')
    term = request.GET.get('search_term', '')
    comm_team_id = request.GET.get('comm_team_id', '')

    if search_for == 'seller' and comm_team_id != -1:
        domain = [['name', 'ilike', term], '|', ['section_manager_ids', 'in', [comm_team_id]], ['section_user_ids', 'in', [comm_team_id]]]
    elif search_for == 'client':
        domain = [['name', 'ilike', term], '|', '|',['customer', '=', True], ['supplier', '=', True], ['is_company', '=', True]]
    else:
        domain = [['name', 'ilike', term]]

    fields = ['id', 'name']
    if search_for == 'address_city':
        fields = ['id', 'name', 'localite_code']

    search_for_mapping = {
        'address_willaya': ['res.country.state', domain, fields],
        'address_city': ['res.localite', domain, fields],
        'address_country': ['res.country', domain, fields],
        'comm_team': ['crm.case.section', domain, fields],
        'seller': ['res.users', domain, fields],
        'company': ['res.company', domain, fields],
        'canal': ['crm.tracking.medium', domain, fields],
        'evenement': ['res.partner', domain, fields],
        'client': ['res.partner', domain, fields]
    }

    model = search_for_mapping.get(search_for)

    if model:
        results = models.execute_kw(db, uid, password, model[0], 'search_read', [model[1]], {'fields': model[2], 'limit': 25})
        #if search_for == 'address_city':
        #    data = [{'id': obj['id'], 'name': obj['name'], 'localite_code': obj['localite_code']} for obj in results]
        #else:
        #    data = [{'id': obj['id'], 'name': obj['name'], 'localite_code': '/'} for obj in results]
        data = [{'id': obj['id'], 'name': obj['name']} for obj in results]
    else:
        data = []

    return JsonResponse(data, safe=False)

@login_required(login_url='users:login')
@admin_only_required
def syn_with_odoo(request):
    
    sync_with_odoo()
    messages.success(request, "Synchronisation réussie!")

    return redirect('users:home')
