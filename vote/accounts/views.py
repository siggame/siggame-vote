from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import login
from django.conf import settings
from django.http import Http404

from .models import State

from urllib import urlencode
import requests


class LoginStageOneView(RedirectView):
    permanent = True

    def get_redirect_url(self, **kwargs):
        state = State.objects.create()
        query_string = urlencode({'client_id': settings.GITHUB_CLIENT_ID,
                                  'state': state})

        return 'https://github.com/login/oauth/authorize?' + query_string


class LoginStageTwoView(RedirectView):
    url = "/"
    permanent = False

    def get(self, request, *args, **kwargs):
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

        payload = {'client_id': settings.GITHUB_CLIENT_ID,
                   'client_secret': settings.GITHUB_CLIENT_SECRET,
                   'code': code}
        response = requests.post('https://github.com/login/oauth/access_token',
                                 headers={'Accept': "application/json"},
                                 data=payload)

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

        # get_or_create returns the instance, and a boolean indicating
        # whether or not the thing was created. we don't care, so use
        # an underscore to throw it away.
        user, _ = User.objects.get_or_create(username=github_username)
        token, _ = GitHubToken.objects.get_or_create(user=user)

        token.token = auth_data['access_token']
        token.save()

        if user.is_active:
            login(request, user)

        # Proceed with the redirect
        super(LoginStageTwoView, self).get(request, *args, **kwargs)
