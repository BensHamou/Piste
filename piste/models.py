from django.db import models
from users.models import CustomUser

class Piste(models.Model):
        
    STATE_PISTE = [
        ('Brouillon', 'Brouillon'),
        ('Confirmé', 'Confirmé'),
        ('Annulé', 'Annulé'),
    ]

    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    object = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    client_id = models.IntegerField(blank=True, null=True)
    client = models.CharField(max_length=255, blank=True, null=True)

    address_street = models.CharField(max_length=255, blank=True, null=True)
    address_street2 = models.CharField(max_length=255, blank=True, null=True)
    address_willaya_id = models.IntegerField(blank=True, null=True)
    address_willaya = models.CharField(max_length=255)
    address_city_id = models.IntegerField(blank=True, null=True)
    address_city = models.CharField(max_length=255, blank=True, null=True)
    address_zip = models.CharField(max_length=255, blank=True, null=True)
    address_country_id = models.IntegerField(blank=True, null=True)
    address_country = models.CharField(max_length=255, blank=True, null=True)

    contact_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    function = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile_phone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    
    seller_id = models.IntegerField(blank=True, null=True)
    seller = models.CharField(max_length=255)
    comm_team_id = models.IntegerField(blank=True, null=True)
    comm_team = models.CharField(max_length=255)
    company_id = models.IntegerField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)

    canal_id = models.IntegerField(blank=True, null=True)
    canal = models.CharField(max_length=255, blank=True, null=True)
    evenement_id = models.IntegerField(blank=True, null=True)
    evenement = models.CharField(max_length=255, blank=True, null=True)
    
    state = models.CharField(choices=STATE_PISTE, max_length=40, blank=True, null=True)

    def __str__(self):
        return self.object

