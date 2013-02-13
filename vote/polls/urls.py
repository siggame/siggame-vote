from django.conf.urls.defaults import patterns, url, include

from .views import ListPollsView


urlpatterns = patterns(
    '',

    url('^$', ListPollsView.as_view(), name="list_polls"),
)
