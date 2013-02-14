from django.db import models
from django.contrib.auth.models import User

from vote.schulze import schulze

from os import urandom
from hashlib import sha1
from datetime import datetime
import json


class VoteManager(models.Manager):
    def closed_now(self):
        return self.filter(closes__lte=datetime.now())

    def upcoming(self):
        return self.filter(opens__gt=datetime.now())

    def open_now(self):
        now = datetime.now()
        return self.filter(opens__lte=now, closes__gt=now)

    def open_to_user(self, user):
        now = datetime.now()
        return self.exclude(already_voted=user).filter(opens__lte=now,
                                                       closes__gt=now)

    def closed_to_user(self, user):
        return self.filter(already_voted=user)


class Vote(models.Model):
    class Meta:
        permissions = (
            ("can_process_ballots", "Can process ballots"),
        )

    objects = VoteManager()

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    opens = models.DateTimeField()
    closes = models.DateTimeField()
    template = models.TextField(blank=True)
    method = models.TextField(blank=True)
    result = models.TextField(blank=True)

    already_voted = models.ManyToManyField(User, null=True,
                                           blank=True)

    def __unicode__(self):
        return self.name

    def needs_processed(self):
        return self.result is None

    def can_user_vote(self, user):
        return not self.already_voted.filter(pk=user.pk).exists()

    def process_ballots(self):
        ballot_data = [json.loads(x.data) for x in self.ballot_set.all()]
        self.result = schulze(ballot_data)
        self.save()
        return self.result


class Ballot(models.Model):
    identifier = models.TextField()
    vote = models.ForeignKey(Vote)
    data = models.TextField()

    def __unicode__(self):
        return self.data

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = sha1(urandom(100)).hexdigest()
        return super(Ballot, self).save(*args, **kwargs)
