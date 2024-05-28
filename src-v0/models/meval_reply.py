#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zzz_lib.zzz_log import zzz_print
from django.db import models
# from . import m_constants_mmr

# from django.apps import apps
# from django.conf import settings
# from django.core.exceptions import ObjectDoesNotExist

# ******************************************************************************
class meval_reply(models.Model):
    display_text        = models.CharField      (max_length=1000)
    meval_question      = models.ForeignKey     ('mmr.meval_question', on_delete=models.CASCADE)
    priority            = models.IntegerField   ()
    score               = models.IntegerField   (default=0)
    # mmh: some way to imply/handle a reply is the default reply that is immediatly checked
    # mmh: without this i think it will be the first replay or lowest prioirity.

    # --------------------------------------------------------------------------
    def __str__(self):
        return_string  = self.display_text + " ( id = " + str(self.id) + ")"
        return format(return_string)











