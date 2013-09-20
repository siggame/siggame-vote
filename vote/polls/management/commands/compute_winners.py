from django.core.management.base import BaseCommand, CommandError
from vote.polls.models import Vote
from vote.schulze import schulze

import json

class Command(BaseCommand):
    help = 'Calculates the winners for each Vote'

    def handle(self, *args, **options):
        self.stdout.write("Winners are determined using Schulze algorithm:\n")
        
        for vote in Vote.objects.all():
            ballots = [json.loads(b.data) for b in vote.ballot_set.all()]
            result = schulze(ballots)

            self.stdout.write("\t{}: {}\n".format(vote.name, result))
