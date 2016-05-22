from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, Sum, F

from api.utils import auth_required

from .forms import CreateListForm, LoginForm, GrantForm

from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from .models import Lister, Item

def index(request):
    '''
        Landing page for all users.

        Display all public lists and allow users
        to create new lists.  Anonymous users
        will be limited in their options to create
        new lists.

        List data will be populated through ajax
        calls to the index_part function below.
    '''
    # Grab all public lists
    lists = Lister.objects.filter(public=True)

    login_form = LoginForm()
    list_form = CreateListForm(authenticated=request.user.is_authenticated())

    storage = messages.get_messages(request)

    # Maintain username if login failed
    for message in storage:
        if message.extra_tags:
            if "login_attempt" in message.extra_tags:
                login_form = LoginForm(login_attempt=message.message)

    context = {
        'lists': lists,
        'login_form': login_form,
        'list_form': list_form
    }

    return render(request, 'lists/index.html', context)


def index_part(request, selection):
    '''
        Return up to date list data for the index page.

        :param selection: indicates whether to return public or user lists
        :type selection: string
    '''
    mine = False

    if selection == "mylists":
        mine = True

    if mine:
        lists = request.user.lister_set.all()
    else:
        lists = Lister.objects.filter(public=True)

    context = {
        'lists': lists,
        'mine': mine
    }

    return render(request, 'lists/index_part.html', context)


#TODO remove this route
def user_lists(request):
    '''
        Return same template as index, but with user lists
        instead of public lists.

        This route should be removed by providing a url
        parameter to the index route, indicating whether
        to return public or private lists.  Especially
        now that the lists are provided by index_part.
    '''
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('lists:index'))

    lists = request.user.lister_set.all()

    list_form = CreateListForm(authenticated=request.user.is_authenticated())
    context = {
        'lists': lists,
        'list_form': list_form,
        'mine': True
    }

    return render(request, 'lists/index.html', context)


def login_user(request):
    '''Authenticate user and redirect to index.'''
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


#TODO rename to register_user for clarity
def register(request):
    '''Register, authenticate, and redirect user to index.'''
    if request.method == 'GET':
        login_form = LoginForm()
        context = {'login_form': login_form}

        return render(request, 'lists/register.html', context)

    elif request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['user']
            password = login_form.cleaned_data['password']

            # Create new user
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

        # Invalid form input
        else:
            context = {'login_form': login_form}
            return render(request, 'lists/register.html', context)

    return HttpResponseRedirect(reverse('lists:index'))


#TODO rename to create_lister for clarity
def create(request):
    '''Create a new list.'''
    if request.method == "POST":
        form = CreateListForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            public = form.cleaned_data['public']
            sortable = form.cleaned_data['sortable']

            user = User.objects.get(username="Anonymous")

            if request.user.is_authenticated():
                user = request.user

            # Create and save list
            lister = Lister(list_name=name, public=public, sortable=sortable, user=user)
            lister.save()

            # Create a group for the list and add the creator if auth
            group_name = "lister-{pk}".format(pk=lister.pk)
            group = Group(name=group_name)
            group.save()

            if request.user.is_authenticated():
                request.user.groups.add(group)

            return HttpResponseRedirect(reverse('lists:lister', args=(lister.id,)))

    return HttpResponseRedirect(reverse('lists:index'))


#TODO rename to grant_users for clarity
@auth_required
def grant(request, list_id):
    '''
        Grant users access to a list.

        :param list_id: id of the list to grant access
        :type list_id: string
    '''
    lister = Lister.objects.get(pk=list_id)

    if request.method == "POST":
        form = GrantForm(request.POST)

        if form.is_valid():
            users_text = form.cleaned_data['users']

            # Split on commas to allow multiple usernames
            users_list = users_text.split(",")

            # Get the group
            group_name = "lister-{pk}".format(pk=lister.pk)
            group = Group.objects.get(name=group_name)

            # Loop over usernames and attempt to add to group
            # Errors will display on the following page
            for username in users_list:
                try:
                    user = User.objects.get(username=username.strip())
                    user.groups.add(group)
                except ObjectDoesNotExist:
                    messages.error(request, '{user} does not exist!'.format(user=username))

    return HttpResponseRedirect(reverse('lists:lister', args=(lister.id,)))


@auth_required
def lister(request, list_id):
    '''
        Display the contents of individual lists.

        This page will allow the user to view the entries
        in a list.  THe user will also be able to vote,
        sort, add items, and grant permission to other users
        depending on ownership and access.

        Item data will be populated through ajax
        calls to the index_part function below.

        :param list_id: id of the list to display
        :type list_id: string
    '''
    lister = Lister.objects.get(pk=list_id)

    if request.method == 'GET':
        mine = False

        if request.user == lister.user:
            mine = True

        login_form = LoginForm()
        grant_form = GrantForm()

        context = {
            'list_id': list_id,
            'lister': lister.list_name,
            'login_form': login_form,
            'grant_form': grant_form,
            'mine': mine,
            'sortable': lister.sortable
        }

        return render(request, 'lists/lister.html', context)

    elif request.method == 'POST':
        text = request.POST['add']

        # Add item to the list
        if text != "":
            if lister.sortable:

                # First item in sortable should be index 1
                if lister.item_set.all().count() == 0:
                    lister.item_set.create(item_text=text, votes=1)

                # If not first, index is one more than current max
                else:
                    rank = lister.item_set.all().aggregate(Max('votes'))['votes__max'] + 1
                    lister.item_set.create(item_text=text, votes=rank)

            # Regular list items start with 0 votes
            else:
                lister.item_set.create(item_text=text, votes=0)

        return HttpResponseRedirect(reverse('lists:lister', args=(list_id,)))


#TODO rename to lister_part for clarity
@auth_required
def part(request, list_id):
    '''
        Return up to date item data for the lister page.

        :param list_id: id of the list to display
        :type list_id: string
    '''
    lister = Lister.objects.get(pk=list_id)

    num_votes = None
    voted = None

    if lister.sortable:
        items = lister.item_set.all().order_by('votes')
    else:
        items = lister.item_set.all().order_by('-votes')
        num_votes = items.aggregate(Sum('votes'))

    for item in items:
        if request.user.is_authenticated():
            if item.users.filter(pk=request.user.pk).exists():
                voted = item.item_text
        else:
            if item.sessions.filter(session_key=request.session.session_key).exists():
                voted = item.item_text

    mine = False

    if request.user == lister.user:
        mine = True

    context = {
        'items': items,
        'list_id': list_id,
        'lister': lister.list_name,
        'num_votes': num_votes,
        'voted': voted,
        'mine': mine,
        'sortable': lister.sortable
    }

    return render(request, 'lists/lister_part.html', context)


@csrf_exempt
@auth_required
def vote(request, list_id, item_id, action):
    '''
        Process actions on list votes.

        Allow users to upvote, downvote, and delete items.
        Votes will store session or user data in the items
        in order to persist.

        :param list_id: id of the list that contains the item
        :type list_id: string
        :param item_id: id of the item to perform action
        :type item_id: string
        :param action: type of action to perform on the item
        :type action: string
    '''
    item = get_object_or_404(Item, pk=item_id)
    lister = Lister.objects.get(pk=list_id)

    if action == "up":
        item.votes += 1

        # Add user or anonymous session to item for persistence
        if request.user.is_authenticated():
            item.users.add(request.user)
        else:
            request.session.save() # session_key is invalid unless saved
            session = Session.objects.get(session_key=request.session.session_key)
            item.sessions.add(session)

    elif action == "down" and item.votes > 0:
        item.votes -= 1

        # Remove user or anonymous session from item
        if request.user.is_authenticated():
            item.users.remove(request.user)
        else:
            session = Session.objects.get(session_key=request.session.session_key)
            item.sessions.remove(session)

    if action == "delete":
        item.delete()

    else:
        item.save()

    return HttpResponseRedirect(reverse('lists:part', args=(list_id,)))


# TODO rename to sort_items for clarity
@csrf_exempt
@auth_required
def sort(request, list_id, old_index, new_index):
    '''
        Reorder sortable lists in the database.

        Take the old and new index returned from the Sortable
        object and update list votes accordingly.

        Index values start at 0, but list votes start at 1.
        All logic includes +1 indexing for votes.

        :param list_id: id of the list to be sorted
        :type list_id: string
        :param old_index: 0 base index of where the item is
        :type old_index: string
        :param new_index: 0 base index of where the item should be placed
        :type new_index: string
    '''
    old_index = int(old_index)
    new_index = int(new_index)

    if request.method == "POST":
        lister = Lister.objects.get(pk=list_id)

        # Temporarily set the old index to 0.  This prevents
        # accidental updates in the filter ranges below
        lister.item_set.filter(votes=old_index+1).update(votes=0)

        # Update ranges depending on which index is greater
        if old_index > new_index:
            lister.item_set.filter(votes__range=(new_index+1,old_index)).update(votes=F('votes') + 1)

        else:
            lister.item_set.filter(votes__range=(old_index+2,new_index+1)).update(votes=F('votes') - 1)

        # Update the item that was moved and temporarily set to 0
        lister.item_set.filter(votes=0).update(votes=new_index+1)

    return HttpResponseRedirect(reverse('lists:part', args=(list_id,)))


#TODO rename to delete_lister for clarity
@csrf_exempt
@auth_required
def delete(request, list_id):
    '''Remove an entire list by list_id.'''
    if request.method == "POST":
        lister = Lister.objects.get(pk=list_id)
        lister.delete()

    return HttpResponseRedirect(reverse('lists:index_part', args=("mylists",)))


#TODO rename to clear_votes for clarity
@csrf_exempt
@auth_required
def clear(request, list_id):
    '''Clear all of the votes from a list by list_id.'''
    lister = Lister.objects.get(pk=list_id)
    items = lister.item_set.all()
    items.update(votes=0)
    [x.users.clear() for x in items]
    [x.sessions.clear() for x in items]

    return HttpResponseRedirect(reverse('lists:part', args=(list_id,)))


def api(request):
    '''Display page to generate API token.'''
    return render(request, 'lists/api.html')
