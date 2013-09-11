# -*- coding: utf-8 -*-
import views
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^set_currency/$',     views.set_currency),
)
