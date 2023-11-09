from xmlrpc import client
from .models import Piste
from django.core.mail import send_mail
from django.utils.html import format_html
from datetime import datetime

url = "http://10.20.10.43:8069"
#url = "http://10.23.10.101:8014"
db = 'hasnaoui'
username = "admin"
password = "28lWcgk9Np3D"

common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def sync_with_odoo():
    # get all pistes that state = confirmed and odoo_id is null
    defaults = {
        'country_id': 63,
        'medium_id': 6,
        'stage_id': 1,
    }
    # get pistes that state = confirmed AND odoo_id is not defined

    pistes = Piste.objects.filter(state='Confirmé', odoo_id=None)
    created_pistes = []
    for piste in pistes:
        data = {
            'name': piste.object if piste.object else None,
            'partner_name': piste.company_name if piste.company_name else None,
            'contact_name': piste.contact_name if piste.contact_name else None,
            'partner_id': piste.client_id if piste.client else None,
            'street': piste.address_street if piste.address_street else None,
            'street2': piste.address_street2 if piste.address_street2 else None,
            'city': piste.address_city_id if piste.address_city else None,
            'state': piste.address_willaya_id if piste.address_willaya else None,
            'zip': piste.address_zip if piste.address_zip else None,
            'country_id': piste.address_country_id if piste.address_country else defaults['country_id'],
            'email_from': piste.email if piste.email else None,
            'function': piste.function if piste.function else None,
            'phone': piste.phone if piste.phone else None,
            'mobile': piste.mobile_phone if piste.mobile_phone else None,
            'fax': piste.fax if piste.fax else None,
            'section_id': piste.comm_team_id if piste.comm_team else None,
            'company_id': piste.company_id if piste.company else None,
            'medium_id': piste.company_id if piste.company else defaults['medium_id'],
            'user_id': piste.seller_id if piste.seller else None,
            'description': piste.note_intern if piste.note_intern else '',
            'stage_id': defaults['stage_id']
        }
        data = {key: value for key, value in data.items() if value is not None}

        piste_id = models.execute_kw(db, uid, password, "crm.lead", "create", [data])

        piste.odoo_id = piste_id

        piste.save()

        created_pistes.append({'id': piste.pk, 'odoo_id': piste.odoo_id})

    recipient_list = ['benshamou@gmail.com']

    if len(created_pistes) > 0 :
        subject = 'Notification de synchronisation ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        address = 'http://127.0.0.1:8000/pistes/detail-piste/'
        message = '''<p>Salam,<br> 
Au total, '''+str(len(created_pistes))+''' pistes ont été synchronisées avec succès avec Odoo:'''
        for cp in created_pistes:
            #addressOdoo = 'http://10.23.10.101:8014/web#id=XXXX&view_type=form&model=crm.lead&menu_id=477&action=565'
            addressOdoo = 'http://10.20.10.43:8069/web#id=XXXX&view_type=form&model=crm.lead&menu_id=477&action=565'
            message += '''<br> - Platform: '''+address + str(cp['id'])+''' => Odoo: '''+addressOdoo.replace('XXXX', str(cp['odoo_id']))
        
        message += '''<br> Toutes ces pistes ont été créées en tant que 'Nouveau', pensez à les consulter afin de compléter d'éventuelles informations manquantes.
        <br> 
        Cordiallement'''


        formatHtml = format_html(message)
        send_mail(subject, "", 'CRM Event', recipient_list, html_message=formatHtml)        