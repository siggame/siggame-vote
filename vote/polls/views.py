from django.views.generic import TemplateView


class ListPollsView(TemplateView):
    template_name = "polls/list_polls.html"


from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Vote, Ballot, UserVoted


@login_required
def list_polls(request):
    now = datetime.now()
    closed_votes = Vote.objects.filter(closes__lte=now)
    upcoming_votes = Vote.objects.filter(opens__gt=now)
    open_votes = Vote.objects.filter(opens__lte=now).filter(closes__gt=now)

    # this is terrible, how do I filtered django?
    open_votes = set(open_votes)
    my_vote_things = UserVoted.objects.filter(user=request.user)
    my_votes = set([x.vote for x in my_vote_things])
    needy_votes = open_votes - my_votes
    filled_votes = open_votes & my_votes

    payload = {'needy_votes': needy_votes,
               'filled_votes': filled_votes,
               'upcoming_votes': upcoming_votes,
               'closed_votes': closed_votes}
    return render_to_response("polls/list_polls.html", payload)


def view_vote_info(request, vote_id):  # for upcoming and filled votes
    vote = get_object_or_404(Vote, pk=vote_id)
    return render_to_response('polls/view_poll_info.html', {'vote': vote})


def view_vote_results(request, vote_id):  # for closed votes
    vote = get_object_or_404(Vote, pk=vote_id)
    return render_to_response('polls/view_poll_results.html', {'vote': vote})


def get_ballot(request, vote_id):  # for needy votes
    return HttpResponse("cute under construction gif goes here!")


from vote.schulze import schulze


# I'm a terrible person for putting this here
def process_ballots(vote_id):
    vote = Vote.objects.get(pk=vote_id)
    ballots = [x.data for x in Ballot.objects.filter(vote=vote)]
    vote.result = schulze(ballots)
    vote.save()
    return vote.result
