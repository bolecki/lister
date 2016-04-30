from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout

from .forms import CreateListForm, LoginForm

from django.contrib.auth.models import User
from .models import Lister, Item

def index(request):
    lists = Lister.objects.filter(public=True)
    login_form = LoginForm()
    list_form = CreateListForm(authenticated=request.user.is_authenticated())
    context = {
        'lists': lists,
        'list_form': list_form,
        'login_form': login_form
    }

    if request.method == 'GET':
        if request.user.is_authenticated():
            context['user'] = request.user
            context['lists'] = request.user.lister_set.all()

    return render(request, 'lists/login.html', context)


def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['user']
            password = login_form.cleaned_data['password']

            # Check for existing user and authenticate
            try:
                User.objects.get(username=username)
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)

            # User does not exist
            except ObjectDoesNotExist:
                pass

    return HttpResponseRedirect(reverse('lists:index'))


def register(request):
    if request.method == 'GET':
        login_form = LoginForm()
        context = {'login_form': login_form}

        return render(request, 'lists/register.html', context)

    elif request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['user']
            password = login_form.cleaned_data['password']

            if User.objects.filter(username=username).count() == 0:
                user = User(username=username)
                user.set_password(password)
                user.save()

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)

            # User already taken
            else:
                pass

    return HttpResponseRedirect(reverse('lists:index'))


def create(request):
    if request.method == "POST":
        form = CreateListForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            public = form.cleaned_data['public']

            lister = Lister(list_name=name, public=public)
            lister.save()

            return HttpResponseRedirect(reverse('lists:lister', args=(lister.id,)))

    return HttpResponseRedirect(reverse('lists:index'))


def lister(request, list_id):
    lister = Lister.objects.get(pk=list_id)

    if request.method == 'GET':
        items = lister.item_set.all().order_by('-votes')
        context = {'items': items, 'list_id': list_id, 'lister': lister.list_name}

        return render(request, 'lists/index.html', context)

    elif request.method == 'POST':
        text = request.POST['add']

        if text != "":
            lister.item_set.create(item_text=text, votes=0)

        return HttpResponseRedirect(reverse('lists:lister', args=(list_id,)))


def vote(request, list_id, item_id, action):
    item = get_object_or_404(Item, pk=item_id)

    if action == "up":
        item.votes += 1
    elif action == "down" and item.votes > 0:
        item.votes -= 1

    if action == "delete":
        item.delete()
    else:
        item.save()

    return HttpResponseRedirect(reverse('lists:lister', args=(list_id,)))
