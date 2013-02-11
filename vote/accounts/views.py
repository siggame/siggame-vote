from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import login
from django.conf import settings
from django.http import Http404

from .models import State, GitHubToken

from urllib import urlencode
import requests


class LoginStageOneView(RedirectView):
    permanent = True

    def get_redirect_url(self, **kwargs):
        # Start by redirecting the user to GitHub to sign in
        # We create a State object to store the random state string.
        # If we get a different state string later, we'll know something fishy
        # is happening.
        state = State.objects.create()
        query_string = urlencode({'client_id': settings.GITHUB_CLIENT_ID,
                                  'state': state})

        return 'https://github.com/login/oauth/authorize?' + query_string


class LoginStageTwoView(RedirectView):
    url = "/"
    permanent = False

    def get(self, request, *args, **kwargs):
        # Once the user signs in, GitHub redirects them here,
        # passing a "code" query parameter and "state" query parameter
        # We grab the code, and verify that the state string is the
        # same one that we sent earlier.
        try:
            code = request.GET['code']
            pk, state_hash = request.GET['state'].split('|')
            state = State.objects.get(pk=pk, state_hash=state_hash)
        except KeyError:
            raise Http404('Either code or state not provided')
        except ValueError:
            raise Http404('Unable to unpack state')
        except State.DoesNotExist:
            raise Http404('Invalid state. BAIL!')

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
            assert 'token_type' in auth_data
            assert 'access_token' in auth_data
        except ValueError:
            raise Http404('Could not decode JSON.')
        except AssertionError:
            raise Http404('Did not receive token back from GitHub')

        response = requests.get("https://api.github.com/user/",
                                params=auth_data)
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

        github.token = auth_data['access_token']
        github.save()

        # Use Django's login() function to set up any necessary session crap
        if user.is_active:
            login(request, user)

        # Proceed with the redirect to the home page.
        # This is a RedirectView, after all
        return super(LoginStageTwoView, self).get(request, *args, **kwargs)
