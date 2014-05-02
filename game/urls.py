from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('game.views',

    url(r'^game/over/', 'game_over', # Order matters! If game/ first, will match that first!
    	name='game_over'),
    url(r'^game/', 'game',
    	name='game'),

)