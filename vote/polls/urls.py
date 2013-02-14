from django.conf.urls.defaults import patterns, url, include

from .views import (ListPollsView, VoteDetailView, VoteResultsView,
                    CreateBallotView, BallotDetailView)


urlpatterns = patterns(
    '',

    url('^$', ListPollsView.as_view(),
        name="list_polls"),
    url(r'^vote_info/(?P<vote_id>\d+)$', VoteDetailView.as_view(),
        name='detail_poll'),
    url(r'^vote_results/(?P<vote_id>\d+)$', VoteResultsView.as_view(),
        name='detail_poll_results'),
    url(r'^get_ballot/(?P<vote_id>\d+)$', CreateBallotView.as_view(),
        name='submit_ballot'),
    url(r'^ballot/(?P<ballot_id>[a-f0-9]{40})$', BallotDetailView.as_view(),
        name='detail_ballot'),
)
