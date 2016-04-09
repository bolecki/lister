from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Item

def index(request):
    items = Item.objects.all()
    output = "<br>".join([i.list_text for i in items])
    return HttpResponse(output)
