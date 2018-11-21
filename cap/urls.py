# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

# Create your urls here.

urlpatterns = [
	url(r'^$',views.index,name='index'),
    url(r'^Step2$',views.Step2,name='step2'),
    url(r'^Step3$',views.Step3,name='step3')
    ]
