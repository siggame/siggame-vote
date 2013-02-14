from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


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

    def can_user_vote(self, user):
        return not self.already_voted.filter(pk=user.pk).exists()


class Ballot(models.Model):
    identifier = models.TextField()
    vote = models.ForeignKey(Vote)
    data = models.TextField()

    def __unicode__(self):
        return self.data
