from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Item

def index(request):
    if request.method == 'GET':
        items = Item.objects.all().order_by('-votes')
        context = {'items': items}
        return render(request, 'lists/index.html', context)
    elif request.method == 'POST':
        text = request.POST['add']
        if text != "":
            i = Item(list_text=text)
            i.save()
        return HttpResponseRedirect(reverse('lists:index'))

def vote(request, item_id, action):
    item = get_object_or_404(Item, pk=item_id)
    if action == "up":
        item.votes += 1
    elif action == "down" and item.votes > 0:
        item.votes -= 1

    if action == "delete":
        item.delete()
    else:
        item.save()
    return HttpResponseRedirect(reverse('lists:index'))
