#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from django.conf.urls import include #, url

from .views import vassessment_urls, vdev_urls

# ========================= final url declaration
urlpatterns = [
    path("va/",         include(vassessment_urls)),
    path("vdev/",       include(vdev_urls)),
]

