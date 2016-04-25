from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .utils import FilteredSerializer
from django.db.models import Max

from lists.models import Lister, Item

serializer = FilteredSerializer()

def index(request, list_id):
    lister = Lister.objects.get(pk=list_id)
    items = lister.item_set.all().order_by('-votes')
    data = serializer.serialize(items, fields=('item_text', 'votes'))
    
    return HttpResponse(data);

def random(request, list_id, option="default"):
    lister = Lister.objects.get(pk=list_id)
    items = lister.item_set.all()

    if option == "tie":
        max_votes = items.aggregate(Max('votes'))['votes__max']
        tied = items.filter(votes=max_votes)
        item = tied.order_by('?').first()

        return HttpResponse(item)

    else:
        item = items.order_by('?').first()

        return HttpResponse(item)
