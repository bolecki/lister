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
        self.user = User.objects.create_user(
            username='tester', password='top_secret')

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
