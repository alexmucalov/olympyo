from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('home.views',

    url(r'^$', 'home'),
)



