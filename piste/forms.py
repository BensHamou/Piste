from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import *
from django.utils import timezone
from django.db.models import Q

def getAttrs(type, placeholder='', other={}):
    ATTRIBUTES = {
        'control': {'class': 'form-control', 'style': 'background-color: #fcfffe;', 'placeholder': ''},
        'search': {'class': 'form-control form-input', 'style': 'background-color: rgba(202, 207, 215, 0.5); border-color: transparent; box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); color: #f2f2f2; height: 40px; text-indent: 33px; border-radius: 5px;', 'type': 'search', 'placeholder': '', 'id': 'search'},
        'select': {'class': 'form-select', 'style': 'background-color: #cacfd7;'},
        'date': {'type': 'date', 'class': 'form-control dateinput','style': 'background-color: #cacfd7;'},
        'textarea': {"rows": "3", 'style': 'width: 100%', 'class': 'form-control', 'placeholder': '', 'style': 'background-color: #cacfd7;'}
    }

    
    if type in ATTRIBUTES:
        attributes = ATTRIBUTES[type]
        if 'placeholder' in attributes:
            attributes['placeholder'] = placeholder
        if other:
            attributes.update(other)
        return attributes
    else:
        return {}
    
class PisteForm(ModelForm):
    class Meta:
        model = Piste
        fields = ['object',  'company_name', 'client', 'address_street', 'address_street2', 'address_willaya_id', 'address_willaya', 'address_city_id', 'address_city', 'address_zip', 
                  'address_country_id', 'address_country', 'contact_name', 'email', 'function', 'phone', 'mobile_phone', 'fax', 'seller_id', 'seller', 'comm_team_id', 
                  'comm_team', 'company_id', 'company', 'canal_id', 'canal', 'evenement_id', 'evenement']

    object = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Décrivez la piste..')))
    company_name = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Nom de la société')))
    client = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Client')))
    address_street = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Rue..')))
    address_street2 = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','')))
    address_willaya = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Ville')))
    address_city = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Commune')))
    address_zip = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Code postal')))
    address_country = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Pays')))
    
    contact_name = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Nom du contact')))
    email = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Courriel')))
    function = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Fonction')))
    phone = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Téléphone')))
    mobile_phone = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Téléphone mobile')))
    fax = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Fax')))

    comm_team = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Equipe commerciale')))
    seller = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Vendeur')))
    canal = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Canal')))
    evenement = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Evenement')))
    company = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Société')))


    address_willaya_id = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','address_willaya_id')))
    address_city_id = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','address_city_id')))
    address_country_id = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','address_country_id')))
    seller_id = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','seller_id')))
    comm_team_id = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','comm_team_id')))
    company_id = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','company_id')))
    canal_id = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','canal_id')))
    evenement_id = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('control','evenement_id')))


