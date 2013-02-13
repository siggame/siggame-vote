from django.views.generic import RedirectView
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import Http404

from .models import State

from urllib import urlencode


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

        user = authenticate(code=code)
        # Use Django's login() function to set up any necessary session crap
        if user.is_active:
            login(request, user)

        # Proceed with the redirect to the home page.
        # This is a RedirectView, after all
        return super(LoginStageTwoView, self).get(request, *args, **kwargs)
