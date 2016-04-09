from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Item

def index(request):
    if request.method == 'GET':
        items = Item.objects.all()
        context = {'items': items}
        return render(request, 'lists/index.html', context)
    elif request.method == 'POST':
        text = request.POST['add']
        if text != "":
            i = Item(list_text=text)
            i.save()
        return HttpResponseRedirect(reverse('lists:index'))
