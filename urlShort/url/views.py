from django.conf.urls import url
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from .models import UrlData
from django.shortcuts import redirect
import random, string
import redis

rds = redis.Redis(host='localhost', port=6379, db=0)

def redirector(request, hash_id=None):
    hash_code = rds.get(hash_id)
    if hash_code is not None:
        return redirect(hash_code.decode('ascii'))
    
    if UrlData.objects.filter(hash=hash_id).exists():
        url = UrlData.objects.get(hash=hash_id)
        rds.set(hash_id, url.url)
        return redirect(url.url)


def short(long_url):
    N = 7
    s = string.ascii_uppercase + string.ascii_lowercase + string.digits

    # generate a random string of length N
    url_id = ''.join(random.choices(s, k=N))

    # check if hash url already exists
    if not UrlData.objects.filter(slug=url_id).exists():
        # save the data to the model
        create = UrlData.objects.create(url=long_url, slug=url_id)
        return url_id
    else:
        # geneate a random string again
        short(long_url)


@csrf_exempt
def short_url(request):
    long_url = request.POST.get("url")
    hash = short(long_url)
    
    # get the host url
    current_site = get_current_site(request)
    data = {
        "success": True,
        "id": hash,
        "link": f'http://{current_site}//{hash}',
        "long_url": long_url,
    }
    return JsonResponse(data)


def index(request):
    return HttpResponse("<h1 align='center'>URL SHORTNER</h1>")
