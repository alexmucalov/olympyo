from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('game.views',

    url(r'^game/', 'game',
    	name='game'),
)