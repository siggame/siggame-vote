from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import logout

from .views import LoginStageOneView, LoginStageTwoView


urlpatterns = patterns(
    '',
    url('^login/$', LoginStageOneView.as_view(), name="login"),
    url('^login/next/', LoginStageTwoView.as_view(), name="login2"),

    url('^logout/$', logout, {"next_page": "/"}, name="logout"),

)
