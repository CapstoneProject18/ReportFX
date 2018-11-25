# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

# Create your urls here.

urlpatterns = [
	url(r'^Step1$',views.Step1,name='Step1'),
    
    url(r'^Step2$',views.Step2,name='step2'),
    url(r'^Step3$',views.Step3,name='step3'),
    url(r'^Step4$',views.Step4,name='step4'),
    url(r'^Step5$',views.Step5,name='step5'),
    url(r'^',views.index,name='index')
    ]
