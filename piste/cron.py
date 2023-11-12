from .models import Piste, Setting
from django.core.mail import send_mail
from django.utils.html import format_html
from datetime import datetime
from .utils import connect_odoo

def sync_with_odoo():
    defaults = {
        'country_id': 63,
        'medium_id': 6,
        'stage_id': 1,
    }

    pistes = Piste.objects.filter(state='Confirmé', odoo_id=None)
    created_pistes = []
    db, uid, models, password = connect_odoo()
    for piste in pistes:
        data = {
            'name': piste.object if piste.object else None,
            'partner_name': piste.company_name if piste.company_name else None,
            'contact_name': piste.contact_name if piste.contact_name else None,
            'partner_id': piste.client_id if piste.client else None,
            'street': piste.address_street if piste.address_street else None,
            'street2': piste.address_street2 if piste.address_street2 else None,
            'city': piste.address_city_id if piste.address_city else None,
            'state_id': piste.address_willaya_id if piste.address_willaya else None,
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
        try:
            piste_id = models.execute_kw(db, uid, password, "crm.lead", "create", [data])
            piste.odoo_id = piste_id
            piste.save()
            created_pistes.append({'id': piste.pk, 'odoo_id': piste.odoo_id})
        except Exception as e:
            print(e)
            continue

    recipient_list = Setting.objects.filter(name='send_to').values_list('value', flat=True)

    if len(created_pistes) > 0 :
        subject = 'Notification de synchronisation (' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ')'
        address = Setting.objects.get(name='piste_detail').value
        addressOdoo = Setting.objects.get(name='odoo_piste_url').value
        
        message = '''
        <p>Bonjour l'équipe,</p>
        
        <p>Au total, <b>'''+str(len(created_pistes))+''' pistes</b> ont été synchronisées avec succès avec Odoo:
        '''
        for cp in created_pistes:
            message += '''
            <br>    - <a href="'''+address + str(cp['id'])+'''">Platform</a> => <a href="'''+addressOdoo.replace('XXXX', str(cp['odoo_id']))+'''">Odoo</a>'''
        
        message += '''
        <br><br> Toutes ces pistes ont été créées en tant que 'Nouveau', pensez à les consulter afin de compléter d'éventuelles informations manquantes.
        <br> <br> 
        Cordiallement,</p>'''


        formatHtml = format_html(message)
        send_mail(subject, "", 'CRM Event', recipient_list, html_message=formatHtml)        