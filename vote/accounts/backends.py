from django.contrib.auth.models import User
from django.conf import settings

from .models import GitHubToken

import requests
import logging

logger = logging.getLogger(__name__)


class GitHubAuthBackend(object):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, code=None):
        # Then we send a POST to GitHub with our web application's password
        # and the code that they sent us a second ago.
        payload = {'client_id': settings.GITHUB_CLIENT_ID,
                   'client_secret': settings.GITHUB_CLIENT_SECRET,
                   'code': code}
        response = requests.post('https://github.com/login/oauth/access_token',
                                 headers={'Accept': "application/json"},
                                 data=payload)

        # In resonse, GitHub sends us an access token, which we can
        # use to act as the user on GitHub.
        try:
            auth_data = response.json()
            token_type = auth_data['token_type']
            access_token = auth_data['access_token']
        except ValueError:
            logger.error('Could not decode JSON.')
            return None
        except KeyError:
            logger.error('Did not receive token back from GitHub')
            return None

        response = requests.get("https://api.github.com/user",
                                params={'access_token': access_token})
        github_username = response.json()['login']

        # Then, we try to grab a User object to represent the logged
        # in user.  If they've logged in before, grab that
        # object. Otherwise create a new one.  Then, save the
        # access_token for that user with the user object.

        # get_or_create returns the instance, and a boolean indicating
        # whether or not the thing was created. we don't care, so use
        # an underscore to throw it away.
        user, _ = User.objects.get_or_create(username=github_username)
        github, _ = GitHubToken.objects.get_or_create(user=user)

        github.token = access_token
        github.save()

        return user
