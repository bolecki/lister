from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from api.utils import auth_required

from .forms import CreateListForm, LoginForm, GrantForm

from django.contrib.auth.models import User, Group
from .models import Lister, Item

def index(request):
    lists = Lister.objects.filter(public=True)
    login_form = LoginForm()

    storage = messages.get_messages(request)

    # Maintain username if login failed
    for message in storage:
        if message.extra_tags:
            if "login_attempt" in message.extra_tags:
                login_form = LoginForm(login_attempt=message.message)

    list_form = CreateListForm(authenticated=request.user.is_authenticated())
    context = {
        'lists': lists,
        'list_form': list_form,
        'login_form': login_form
    }

    if request.user.is_authenticated():
        context['user'] = request.user

    return render(request, 'lists/login.html', context)


def user_lists(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('lists:index'))

    lists = request.user.lister_set.all()

    list_form = CreateListForm(authenticated=request.user.is_authenticated())
    context = {
        'lists': lists,
        'list_form': list_form,
        'user': request.user,
        'mine': True
    }

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

                    return HttpResponseRedirect(reverse('lists:user_lists'))

                else:
                    messages.info(request, username, extra_tags='login_attempt')
                    messages.error(request, 'Invalid password')


            # User does not exist
            except ObjectDoesNotExist:
                messages.error(request, 'User does not exist - please use the link to register')

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
                messages.error(request, 'User already exists - please select another name')
                return HttpResponseRedirect(reverse('lists:register'))

        else:
            context = {'login_form': login_form}
            return render(request, 'lists/register.html', context)

    return HttpResponseRedirect(reverse('lists:index'))


def create(request):
    if request.method == "POST":
        form = CreateListForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            public = form.cleaned_data['public']

            user = User.objects.get(username="Anonymous")

            if request.user.is_authenticated():
                user = request.user

            lister = Lister(list_name=name, public=public, user=user)
            lister.save()

            group_name = "lister-{pk}".format(pk=lister.pk)
            group = Group(name=group_name)
            group.save()

            if request.user.is_authenticated():
                request.user.groups.add(group)

            return HttpResponseRedirect(reverse('lists:lister', args=(lister.id,)))

    return HttpResponseRedirect(reverse('lists:index'))


@auth_required
def grant(request, list_id):
    lister = Lister.objects.get(pk=list_id)

    if request.method == "POST":
        form = GrantForm(request.POST)

        if form.is_valid():
            users_text = form.cleaned_data['users']
            users_list = users_text.split(",")

            group_name = "lister-{pk}".format(pk=lister.pk)
            group = Group.objects.get(name=group_name)

            for username in users_list:
                try:
                    user = User.objects.get(username=username.strip())
                    user.groups.add(group)
                except ObjectDoesNotExist:
                    messages.error(request, '{user} does not exist!'.format(user=username))

    return HttpResponseRedirect(reverse('lists:lister', args=(lister.id,)))


@auth_required
def lister(request, list_id):
    lister = Lister.objects.get(pk=list_id)

    if request.method == 'GET':
        items = lister.item_set.all().order_by('-votes')
        voted = None

        if request.user.is_authenticated():
            for item in items:
                if item.users.filter(pk=request.user.pk).exists():
                    voted = item.item_text

        grant_form = GrantForm()

        mine = False

        if request.user == lister.user:
            mine = True

        context = {
            'items': items,
            'list_id': list_id,
            'grant_form': grant_form,
            'lister': lister.list_name,
            'voted': voted,
            'mine': mine
        }

        return render(request, 'lists/index.html', context)

    elif request.method == 'POST':
        text = request.POST['add']

        if text != "":
            lister.item_set.create(item_text=text, votes=0)

        return HttpResponseRedirect(reverse('lists:lister', args=(list_id,)))


@auth_required
def vote(request, list_id, item_id, action):
    item = get_object_or_404(Item, pk=item_id)
    lister = Lister.objects.get(pk=list_id)

    if action == "up":
        item.votes += 1

        if request.user.is_authenticated() and not lister.public:
            item.users.add(request.user)

    elif action == "down" and item.votes > 0:
        item.votes -= 1

        if request.user.is_authenticated() and not lister.public:
            item.users.remove(request.user)

    if action == "delete":
        item.delete()
    else:
        item.save()

    return HttpResponseRedirect(reverse('lists:lister', args=(list_id,)))


def api(request):
    return render(request, 'lists/api.html')
