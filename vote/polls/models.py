from django.db import models
from django.contrib.auth.models import User

from vote.schulze import schulze
from vote.accounts.models import GitHubToken
from .validators import validate_ballot

from os import urandom
from hashlib import sha1
from datetime import datetime
import requests
import logging
import json

logger = logging.getLogger(__name__)


id_help = """You need to be an owner of the SIG-Game organization. Go
to https://github.com/organizations/siggame/teams and choose the team
you want to grant permission to. From the URL, grab the id number for
the team. The URL should look like this:

https://github.com/organizations/siggame/teams/:id
"""



class VoteManager(models.Manager):
    def closed_now(self):
        return self.filter(closes__lte=datetime.now())

    def upcoming(self):
        return self.filter(opens__gt=datetime.now())

    def open_now(self):
        now = datetime.now()
        return self.filter(opens__lte=now, closes__gt=now)

    def open_to_user(self, user):
        """Votes that are open and user needs to vote"""
        now = datetime.now()
        return self.exclude(already_voted=user).filter(opens__lte=now,
                                                       closes__gt=now)

    def closed_to_user(self, user):
        """Votes that are open, but this user already voted"""
        now = datetime.now()
        return self.filter(already_voted=user).filter(opens__lte=now,
                                                       closes__gt=now)


class Vote(models.Model):
    class Meta:
        permissions = (
            ("can_process_ballots", "Can process ballots"),
        )

    objects = VoteManager()

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    team_id = models.PositiveIntegerField(help_text=id_help,
                                          null=True)

    created = models.DateTimeField(auto_now_add=True)
    opens = models.DateTimeField()
    closes = models.DateTimeField()
    template = models.TextField(blank=True,
                                validators=[validate_ballot])
    method = models.TextField(blank=True)
    result = models.TextField(blank=True)

    already_voted = models.ManyToManyField(User, null=True,
                                           blank=True)

    def __unicode__(self):
        return self.name

    def needs_processed(self):
        # Returns True if self.result is None or ''
        return not bool(self.result)

    def can_user_view(self, user):
        try:
            endpoint = "https://api.github.com/teams/%d/members" % self.team_id
            params = {'access_token': user.githubtoken.token}
            response = requests.get(endpoint, params=params)
            logger.info("Checking access... GitHub reponse: HTTP %s",
                        response.status_code)
            if response.status_code != 200:
                return False
        except GitHubToken.DoesNotExist:
            logger.info("User %s doesn't have GitHub token", user.username)
        except TypeError:
            logger.info("GitHub team not set for %s", str(self))
        return True

    def can_user_vote(self, user):
        if self.already_voted.filter(pk=user.pk).exists():
            return False
        now = datetime.now()
        if self.opens > now or self.closes < now:
            return False
        return self.can_user_view(user)

    def process_ballots(self):
        ballot_data = [json.loads(x.data) for x in self.ballot_set.all()]
        if ballot_data != []:
            self.result = schulze(ballot_data)
        self.save()
        return self.result


class Ballot(models.Model):
    class Meta:
        ordering = ['?']
    identifier = models.CharField(max_length=40, primary_key=True)
    vote = models.ForeignKey(Vote)
    data = models.TextField()

    def __unicode__(self):
        return self.data

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = sha1(urandom(100)).hexdigest()
        return super(Ballot, self).save(*args, **kwargs)
