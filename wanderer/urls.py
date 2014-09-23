from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^$', 'locations.views.index'),
    url(r'^cards/(?P<slug>[\w\-]+)/$', 'cards.views.card'),
    url(r'^(?P<slug>[\w\-]+)/$', 'locations.views.location'),
)
