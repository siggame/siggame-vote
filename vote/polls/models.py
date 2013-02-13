from django.db import models
from django.contrib.auth.models import User


class Vote(models.Model):
    name = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    opens = models.DateTimeField()
    closes = models.DateTimeField()
    template = models.TextField()
    method = models.TextField()
    result = models.TextField()

    def __unicode__(self):
        return self.name


class Ballot(models.Model):
    identifier = models.TextField()
    vote = models.ForeignKey(Vote)
    data = models.TextField()

    def __unicode__(self):
        return self.data


class UserVoted(models.Model):
    vote = models.ForeignKey(Vote)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.vote.name)
