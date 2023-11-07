from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import *
from django.utils import timezone
from django.db.models import Q

def getAttrs(type, placeholder='', other={}):
    ATTRIBUTES = {
        'control': {'class': 'form-control', 'autocomplete': "off", 'style': 'background-color: #fcfffe;', 'placeholder': ''},
        'controlReq': {'class': 'form-control', 'autocomplete': "off", 'style': 'background-color: #dad2ff; border-color: #dad2ff;', 'placeholder': ''},
        'controlSearch': {'class': 'form-control search-input', 'autocomplete': "off", 'style': 'background-color: #fcfffe;', 'placeholder': ''},
        'controlSearchReq': {'class': 'form-control search-input', 'autocomplete': "off", 'style': 'background-color: #dad2ff; border-color: #dad2ff;', 'placeholder': ''},
        'controlID': {'class': 'form-control search-input-id', 'autocomplete': "off", 'style': 'background-color: #fcfffe;', 'placeholder': ''},
        'controlIDReq': {'class': 'form-control search-input-id', 'autocomplete': "off", 'style': 'background-color: #dad2ff; border-color: #dad2ff;', 'placeholder': ''},
        'search': {'class': 'form-control form-input', 'autocomplete': "off", 'style': 'background-color: rgba(202, 207, 215, 0.5); border-color: transparent; box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); color: #f2f2f2; height: 40px; text-indent: 33px; border-radius: 5px;', 'type': 'search', 'placeholder': '', 'id': 'search'},
        'select': {'class': 'form-select', 'autocomplete': "off", 'style': 'background-color: #fcfffe;'},
        'date': {'type': 'date', 'class': 'form-control dateinput', 'autocomplete': "off" ,'style': 'background-color: #fcfffe;'},
        'textarea': {"rows": "3", 'style': 'width: 100%', 'class': 'form-control', 'autocomplete': "off", 'placeholder': '', 'style': 'background-color: #fcfffe;'}
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
        #fields = ['object',  'company_name', 'client', 'client_id', 'address_street', 'address_street2', 'address_willaya_id', 'address_willaya', 'address_city_id', 'address_city', 'address_zip', 
        #          'address_country_id', 'address_country', 'contact_name', 'email', 'function', 'phone', 'mobile_phone', 'fax', 'seller_id', 'seller', 'comm_team_id', 
        #          'comm_team', 'company_id', 'company', 'canal_id', 'canal', 'evenement_id', 'evenement', 'note_intern']
        
        fields = ['object',  'company_name', 'client', 'client_id', 'address_street', 'address_street2', 'address_willaya_id', 'address_willaya', 
                  'contact_name', 'email', 'function', 'phone', 'mobile_phone', 'fax', 'seller_id', 'seller', 'comm_team_id', 
                  'comm_team', 'note_intern']

    object = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlReq','Décrivez la piste..')))
    company_name = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Nom de la société')), required=False)
    client = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch','Client')), required=False)
    address_street = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Rue..')), required=False)
    address_street2 = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Rue 2..')), required=False)
    address_willaya = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchReq','Willaya')))
    #address_city = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch','Commune')), required=False)
    #address_zip = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Code postal')), required=False)
    #address_country = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch','Pays')), required=False)
    
    contact_name = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlReq','Nom du contact')))
    email = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Courriel')), required=False)
    function = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Fonction')), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Téléphone')), required=False)
    mobile_phone = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlReq','Téléphone mobile')))
    fax = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Fax')), required=False)

    comm_team = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchReq','Équipe commerciale')))
    seller = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchReq','Vendeur')))
    #canal = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch','Canal')), required=False)
    #evenement = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch','Évenement')), required=False)
    #company = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearch','Société')), required=False)


    address_willaya_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID_address_willaya_id')))
    #address_city_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlID','ID_address_city_id')), required=False)
    #address_country_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlID','ID_address_country_id')), required=False)
    seller_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID_seller_id')))
    comm_team_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID_comm_team_id')))
    #company_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlID','ID_company_id')), required=False)
    #canal_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlID','ID_canal_id')), required=False)
    #evenement_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlID','ID_evenement_id')), required=False)
    client_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlID','ID_client_id')), required=False)

    note_intern = forms.CharField(widget=forms.Textarea(attrs= getAttrs('textarea','Notes internes..')), required=False)


