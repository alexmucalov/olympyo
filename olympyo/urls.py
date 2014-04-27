from django.conf.urls import patterns, include, url
from django.http import HttpResponse

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
            # Examples:
            # url(r'^$', 'olympyo.views.home', name='home'),
            # url(r'^blog/', include('blog.urls')),

    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('home.urls')),
    url(r'^', include('lobby.urls')),
    url(r'^', include('game.urls')),
)
