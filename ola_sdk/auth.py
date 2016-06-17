
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import OrderedDict
from random import SystemRandom
from requests import codes
from requests import post
from string import ascii_letters
from string import digits

try:
    from urllib.parse import parse_qs
    from urllib.parse import urlparse
except ImportError:
    from urlparse import parse_qs
    from urlparse import urlparse

from ola_sdk import auth_const as ac
from ola_sdk.helper import build_url


class OAuth2(object):
	
    def __init__(self, client_id, scopes, sandbox=False):
	    self.client_id = client_id
	    self.scopes = scopes
            self.sandbox = sandbox

    def _build_authorization_req_url(
        self,
	response_type,
	redirect_url,
	state=None
    ):
        if response_type in ac.VALID_RESPONSE_TYPES:
            msg = '{} is not a valid response type.'
        
        args = OrderedDict([
            ('scope', ' '.join(self.scopes).replace(' ', ' ')),
            ('state', state),
            ('redirect_uri', redirect_url),
            ('response_type', response_type),
            ('client_id', self.client_id),
            ])
        print (self.sandbox)
        host = ac.TEST_HOST if self.sandbox else ac.AUTH_HOST
        return build_url(host, ac.AUTHORIZE_PATH, args)
    
    def _extract_query(self, redirect_url):

        qs = urlparse(redirect_url)
        qs = qs.fragment
        query_params = parse_qs(qs)
        query_params = {qp: query_params[qp][0] for qp in query_params}
        return query_params


class AccessTokenGrant(OAuth2):

    def __init__(
            self,
            client_id,
            scopes,
            redirect_url,
            state=None,
            sandbox=False,
            ):
        super(AccessTokenGrant, self).__init__(client_id, scopes, sandbox)
        self.redirect_url = redirect_url
        
    def get_authorization_url(self):

        return self._build_authorization_req_url(
                response_type=ac.TOKEN_RESPONSE_TYPE,
                redirect_url=self.redirect_url,
                # state=self.state_token,
        )
