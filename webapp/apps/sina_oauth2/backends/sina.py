"""
Sina weibo OAuth support.

This contribution adds support for sina weibo OAuth service. The settings
SINAWEIBO_APP_ID and SINAWEIBO_API_SECRET must be defined with the values
given by sina weibo application registration process.

Extended permissions are supported by defining SINAWEIBO_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
import logging
logger = logging.getLogger(__name__)

from urllib import urlencode
from urllib2 import urlopen

from django.conf import settings
from django.utils import simplejson
from django.contrib.auth import authenticate

from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
from social_auth.utils import sanitize_log_data


# Sina weibo configuration
EXPIRES_NAME = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')
SINAWEIBO_ME = 'https://api.weibo.com/2/account/profile/basic.json?'


class SinaWeiboBackend(OAuthBackend):
    """Sina weibo OAuth2 authentication backend"""
    name = 'sinaweibo'
    # Default extra data to store
    EXTRA_DATA = [('id', 'id'), ('expires', EXPIRES_NAME)]

    def get_user_details(self, response):
        """Return user details from sina weibo account"""
        return {USERNAME: response.get('username') or response['name'],
                'email': response.get('email', ''),
                'fullname': response['name'],
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', '')
                }

class SinaWeiboAuth(BaseOAuth2):
    """Sina weibo OAuth2 support"""
    AUTH_BACKEND = SinaWeiboBackend
    RESPONSE_TYPE = None
    SCOPE_SEPARATOR = ','
    AUTHORIZATION_URL = 'https://api.weibo.com/oauth2/authorize'
    SETTINGS_KEY_NAME = 'SINAWEIBO_APP_ID'
    SETTINGS_SECRET_NAME = 'SINAWEIBO_API_SECRET'

    def get_scope(self):
        return getattr(settings, 'SINAWEIBO_EXTENDED_PERMISSIONS', [])

    def user_data(self, access_token):
        """Loads user data from service"""
        data = None
        url = SINAWEIBO_ME + urlencode({'access_token': access_token})

        try:
            data = simplejson.load(urlopen(url))
            logger.debug('Found user data for token %s',
                         sanitize_log_data(access_token),
                         extra=dict(data=data))
        except ValueError:
            params.update({'access_token': sanitize_log_data(access_token)})
            logger.error('Could not load user data from sian weibo.',
                         exc_info=True, extra=dict(data=params))
        return data

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if 'code' in self.data:
            """
            url = 'https://api.weibo.com/oauth2/access_token?' + \
                  urlencode({'client_id': settings.SINAWEIBO_APP_ID,
                             'redirect_uri': self.redirect_uri,
                             'client_secret': settings.SINAWEIBO_API_SECRET,
                             'code': self.data['code']})
            """
            url = "https://api.weibo.com/oauth2/access_token"
            params = urlencode({'client_id': settings.SINAWEIBO_APP_ID,
                             'redirect_uri': self.redirect_uri,
                             'client_secret': settings.SINAWEIBO_API_SECRET,
                             'code': self.data['code']})

            response = eval(urlopen(url, params).read())
            access_token = response["access_token"]
            data = self.user_data(access_token)
            if data is not None:
                if 'error' in data:
                    error = self.data.get('error') or 'unknown error'
                    raise ValueError('Authentication error: %s' % error)
                data['access_token'] = access_token
                # expires will not be part of response if offline access
                # premission was requested
                if 'expires' in response:
                    data['expires'] = response['expires'][0]
            kwargs.update({'response': data, self.AUTH_BACKEND.name: True})
            return authenticate(*args, **kwargs)
        else:
            error = self.data.get('error') or 'unknown error'
            raise ValueError('Authentication error: %s' % error)

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking basic settings"""
        return all(hasattr(settings, name) for name in ('SINAWEIBO_APP_ID',
                                                        'SINAWEIBO_API_SECRET'))


# Backend definition
BACKENDS = {
    'sinaweibo': SinaWeiboAuth,
}
