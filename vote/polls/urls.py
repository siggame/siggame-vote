from django.conf.urls.defaults import patterns, url, include

from .views import ListPollsView


urlpatterns = patterns(
    '',

#    url('^$', ListPollsView.as_view(), name="list_polls"),
    url(r'^$', 'vote.polls.views.list_polls'),
    url(r'^vote_info/(?P<vote_id>\d+)$', 'vote.polls.views.view_vote_info'),
    url(r'^vote_results/(?P<vote_id>\d+)$', 'vote.polls.views.view_vote_results'),
    url(r'^get_ballot/(?P<vote_id>\d+)$', 'vote.polls.views.get_ballot'),
)
