#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from .vassessment import *
from .vdev import *

# ============================ vdev_urls
vassessment_urls = [
    path("vassessment_home/<str:string_32>/<int:hack_param>",           vassessment_home,               name="vassessment_home_with_hack_param"),
    path("vassessment_home/<str:string_32>",                            vassessment_home,               name="vassessment_home"),
    path("vassessment_terms/<str:string_32>",                           vassessment_terms,              name="vassessment_terms"),
    path("vassessment_terms_accepted/<str:string_32>",                  vassessment_terms_accepted,     name="vassessment_terms_accepted"),
    path("vassessment_recommendations/<str:string_32>",                 vassessment_recommendations,    name="vassessment_recommendations"),
    # Unused in version 2 of implementation
    # path("vassessment_module_answers/<str:module>/<str:string_32>",     vassessment_module_answers,     name="vassessment_module_answers"),
    # path("vassessment_module_questions/<str:module>/<str:string_32>",   vassessment_module_questions,   name="vassessment_module_questions"),
]

# ============================ vdev_urls
vdev_urls = [
    path("vdev_home",                           vdev_home,                          name="vdev_home"),
    path("vdev_removedefaultdata",              vdev_removedefaultdata,             name="vdev_removedefaultdata"),
    path("vdev_createdefaultdata",              vdev_createdefaultdata,             name="vdev_createdefaultdata"),
    path("vdev_sendtestemail",                  vdev_sendtestemail,                 name="vdev_sendtestemail"),
    path("vdev_listfailedemails",               vdev_listfailedemails,              name="vdev_listfailedemails"),
    path("vdev_resendfailedemails",             vdev_resendfailedemails,            name="vdev_resendfailedemails"),
    path("vdev_displayenvbuildvariables",       vdev_displayenvbuildvariables,      name="vdev_displayenvbuildvariables"),
    path("vdev_logs/<str:filename>",            vdev_logs,                          name="vdev_logs"),
    path("vdev_logs",                           vdev_logs,                          name="vdev_logs"),
    path("vdev_displaysettings",                vdev_displaysettings,               name="vdev_displaysettings"),
    path("vdev_testingview",                    vdev_testingview,                   name="vdev_testingview"),
]
