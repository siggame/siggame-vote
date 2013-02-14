from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Vote, Ballot
from .forms import BallotForm


class ListPollsView(TemplateView):
    template_name = "polls/list_polls.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListPollsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListPollsView, self).get_context_data(**kwargs)

        context['closed_votes'] = Vote.objects.closed_now()
        context['upcoming_votes'] = Vote.objects.upcoming()
        context['needy_votes'] = Vote.objects.open_to_user(self.request.user)
        context['filled_votes'] = Vote.objects.closed_to_user(self.request.user)

        return context


class VoteDetailView(DetailView):
    pk_url_kwarg = 'vote_id'
    model = Vote
    template_name = 'polls/view_poll_info.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(VoteDetailView, self).dispatch(*args, **kwargs)


class VoteResultsView(VoteDetailView):
    template_name = 'polls/view_poll_results.html'


class CreateBallotView(CreateView):
    model = Ballot
    template_name = "polls/get_ballot.html"
    form_class = BallotForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        try:
            self.vote = Vote.objects.get(pk=kwargs['vote_id'])
        except Vote.DoesNotExist:
            raise Http404("Derp. No vote object.")
        except KeyError:
            raise Http404("No vote_id provided")

        request = args[0]
        if not self.vote.can_user_vote(request.user):
            raise Http404("User can't vote!")

        return super(CreateBallotView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return "/"

    def get_context_data(self, **kwargs):
        context = super(CreateBallotView, self).get_context_data(**kwargs)
        context['vote'] = self.vote
        return context

    def get_form_kwargs(self):
        form_kwargs = super(CreateBallotView, self).get_form_kwargs()
        form_kwargs['instance'] = Ballot(vote=self.vote)
        return form_kwargs

    def form_valid(self, form):
        redirect = super(CreateBallotView, self).form_valid(form)
        self.vote.already_voted.add(self.request.user)
        return redirect

from vote.schulze import schulze
import json


# I'm a terrible person for putting this here
def process_ballots(vote_id):
    vote = Vote.objects.get(pk=vote_id)
    ballots = [json.loads(x.data) for x in Ballot.objects.filter(vote=vote)]
    vote.result = schulze(ballots)
    vote.save()
    return vote.result



# click on link. link takes you to form.
# form shows the vote, and the example ballot
# instructs user to copy example ballot
# manipulate order of entries so prefered items are further to the left
# and paste fixed ballot into textbox
# press submit
# unique identifier generated, ballot stored, UserVoted generated
# user is shown the ballot that was submitted, including identifier
# user told that identifier is not linked to user by the system, and that
# they need to copy it down right now if they want to audit later.
# link provided to get back to votes page
