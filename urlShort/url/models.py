from django.db import models

class UrlData(models.Model):
    '''
        URLData model have two data fields - original url
        and its corresponding short url (slug)
    '''
    url = models.CharField(max_length=200)
    slug = models.CharField(max_length=15) # Short URL

    class Meta:
        db_table = 'url_shortner'