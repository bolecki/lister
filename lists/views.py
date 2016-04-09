from django.shortcuts import render
from .models import Item

def index(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'lists/index.html', context)
