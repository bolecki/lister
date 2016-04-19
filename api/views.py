from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Max

from lists.models import Item

def index(request):
    items = Item.objects.all().order_by('-votes')
    data = serializers.serialize("json", items)
    
    return HttpResponse(data);

def random(request, option):
    if option == "tie":
        max_votes = Item.objects.all().aggregate(Max('votes'))['votes__max']
        items = Item.objects.filter(votes=max_votes)
        item = items.order_by('?').first()
        return HttpResponse(item)
    else:
        items = Item.objects.all().order_by('-votes')
        item = items.order_by('?').first()
        return HttpResponse(item)
