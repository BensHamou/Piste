from django.db import models

class Piste(models.Model):
        
    STATE_PISTE = [
        ('Brouillon', 'Brouillon'),
        ('Confirmé', 'Confirmé'),
        ('Annulé', 'Annulé'),
    ]

    object = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    client = models.CharField(max_length=255)

    address_street = models.CharField(max_length=255)
    address_street2 = models.CharField(max_length=255)
    address_willaya_id = models.IntegerField()
    address_willaya = models.CharField(max_length=255)
    address_city_id = models.IntegerField()
    address_city = models.CharField(max_length=255)
    address_zip = models.CharField(max_length=255)
    address_country_id = models.IntegerField()
    address_country = models.CharField(max_length=255)

    contact_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    function = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    mobile_phone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    seller_id = models.IntegerField()
    seller = models.CharField(max_length=255)
    comm_team_id = models.IntegerField()
    comm_team = models.CharField(max_length=255)
    company_id = models.IntegerField()
    company = models.CharField(max_length=255)

    canal_id = models.IntegerField()
    canal = models.CharField(max_length=255)
    evenement_id = models.IntegerField()
    evenement = models.CharField(max_length=255)
    
    state = models.CharField(choices=STATE_PISTE, max_length=40)

    def __str__(self):
        return self.object

