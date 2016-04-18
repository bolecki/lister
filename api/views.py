from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core import serializers

from lists.models import Item

def index(request):
    items = Item.objects.all().order_by('-votes')
    data = serializers.serialize("json", items)
    
    return HttpResponse(data);
