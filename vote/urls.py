from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^accounts/', include('vote.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )
