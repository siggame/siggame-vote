from django.conf.urls.defaults import patterns, url, include

from .views import LoginStageOneView, LoginStageTwoView


urlpatterns = patterns(
    '',

    url('^login/$', LoginStageOneView.as_view(), name="login1"),
    url('^login/next/', LoginStageTwoView.as_view(), name="login2"),
)
