from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from lists.models import Lister, Item

import lists.views


class TestUser(object):
    is_auth = False

    def __init__(self, authenticated=False):
        self.is_auth = authenticated

    def is_authenticated(self):
        return self.is_auth


class IndexTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.public_user = User.objects.create_user(username="Anonymous", password="testpass")

    def test_authenticated_index(self):
        request = self.factory.get('/lists')
        request.user = TestUser(authenticated=True)
        response = lists.views.index(request)

        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<label for="id_sortable">Sortable:</label>', response.content)

    def test_anonymous_index(self):
        request = self.factory.get('/lists')
        request.user = TestUser(authenticated=False)
        response = lists.views.index(request)

        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<input id="id_sortable" name="sortable" type="hidden" value="False" />', response.content)


class IndexPartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.public_user = User.objects.create_user(username="Anonymous", password="testpass")
        self.public_user = User.objects.create_user(username="public-user", password="testpass")
        self.private_user = User.objects.create_user(username="private-user", password="testpass")
        Lister.objects.create(list_name="public", public=True, user=self.public_user)
        Lister.objects.create(list_name="private", user=self.private_user)

    def test_public_index_part(self):
        request = self.factory.get('/lists/index-part/public')
        request.user = self.public_user
        response = lists.views.index_part(request, 'public')

        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<small> - public-user</small>', response.content)
        self.assertInHTML('<small></small>', response.content, count=0)

    def test_private_index_part(self):
        request = self.factory.get('/lists/index-part/mylists')
        request.user = self.private_user
        response = lists.views.index_part(request, 'mylists')

        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<small></small>', response.content)
        self.assertInHTML('<small> - public-user</small>', response.content, count=0)
