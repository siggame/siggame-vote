from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from os import urandom
from hashlib import sha1
import requests
import logging

logger = logging.getLogger(__name__)


def generate_state():
    return sha1(urandom(100)).hexdigest()


# Create your models here.
class State(models.Model):
    state_hash = models.CharField(max_length=40,
                                  default=generate_state)

    def __str__(self):
        return "%d|%s" % (self.pk, self.state_hash)


class GitHubToken(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=40, null=True)

    def _get(self, path, params=None):
        if params is None:
            params = {}
        params.update({'access_token': self.token})
        resp = requests.get(path, params=params)
        return resp.json()

    @property
    def organizations(self):
        return [x['login'] for x in self._get("/user/orgs")]


@receiver(user_logged_out)
def delete_github_token(sender, request, user, **kwargs):
    """Deletes the token when the user logs out."""
    try:
        GitHubToken.objects.get(user=user).delete()
    except GitHubToken.DoesNotExist:
        logger.warning("No token to delete... that's weird.")
