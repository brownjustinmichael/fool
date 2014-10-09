from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^$', 'locations.views.index'),
    url(r'^shuffle/$', 'cards.views.shuffle'),
    url(r'^draw/$', 'cards.views.draw'),
    url(r'^cards/(?P<slug>[\w\-]+)/$', 'cards.views.card'),
    url(r'^exploration/(?P<slug>[\w\-]+)/draw/$', 'locations.views.draw'),
    url(r'^exploration/(?P<slug>[\w\-]+)/shuffle/$', 'locations.views.shuffle'),
    url(r'^exploration/(?P<slug>[\w\-]+)/$', 'locations.views.location'),
)
