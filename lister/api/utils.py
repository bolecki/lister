# The MIT License (MIT)

# Copyright (c) 2015 Nikunj Handa

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token

from lists.models import Lister


def json_response(response_dict, status=200):
    response = HttpResponse(json.dumps(response_dict), content_type="application/json", status=status)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

    return response


def auth_required(func):
    def inner(request, *args, **kwargs):
        api = False

        if request.path.split("/")[1] == "api":
            api = True

        if 'list_id' in kwargs:
            lister = Lister.objects.get(pk=kwargs['list_id'])

            if lister:
                if lister.public:
                    return func(request, *args, **kwargs)

                elif request.user.is_authenticated():
                    group_name = "lister-{pk}".format(pk=lister.pk)

                    if request.user.groups.filter(name=group_name).count() == 1:
                        return func(request, *args, **kwargs)

        if request.method == 'OPTIONS':
            return func(request, *args, **kwargs)

        auth_header = request.META.get('HTTP_AUTHORIZATION', None)

        if auth_header is not None:
            tokens = auth_header.split(' ')

            if len(tokens) == 2 and tokens[0] == 'Token':
                token = tokens[1]

                try:
                    request.token = Token.objects.get(key=token)
                    return func(request, *args, **kwargs)

                except Token.DoesNotExist:
                    return json_response({
                        'error': 'Token not found'
                    }, status=401)

        if api:
            return json_response({
                'error': 'Invalid Header'
            }, status=401)
        else:
            return HttpResponseRedirect(reverse('lists:index'))

    return inner
