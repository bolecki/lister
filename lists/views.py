from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Item

def index(request):
    items = Item.objects.all()
    template = loader.get_template('lists/index.html')
    context = {
        'items': items,
    }
    return HttpResponse(template.render(context, request))
