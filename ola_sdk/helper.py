from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from json import dumps
from requests import Request

try:
    from urllib.parse import quote
    from urllib.parse import urlencode
    from urllib.parse import urljoin
except ImportError:
    from urllib import quote
    from urllib import urlencode
    from urlparse import urljoin


def build_url(host, path, params=None):

    path = quote(path)
    params = params or {}

    if params:
        path = '/{}?{}'.format(path, urlencode(params))
    else:
        path = '/{}'.format(path)
    # path = path.replace('+', '%20')

    return urljoin(host, path)
