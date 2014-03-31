from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('lobby.views',

    url(r'^lobby/', 'lobby'),
    url(r'^waitroom/', 'waitroom'),
)