#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zzz_lib.zzz_log import zzz_print
from django import forms
from django.db import models

# from . import m_constants_mmr
# from django.apps import apps
# from django.conf import settings
# from django.core.exceptions import ObjectDoesNotExist
# from django.forms import BaseModelFormSet

# ******************************************************************************
class meval_question(models.Model):
    display_text        = models.CharField      (max_length=1000)
    meval_module        = models.ForeignKey     ('mmr.meval_module', on_delete=models.CASCADE)
    priority            = models.IntegerField   ()

    # --------------------------------------------------------------------------
    def __str__(self):
        return_string  = self.display_text + " ( id = " + str(self.id) + ")"
        return format(return_string)

    # --------------------------------------------------------------------------
    def get_querystring_of_meval_reply(self):
        from ..models import meval_reply
        qs = meval_reply.objects \
            .filter(meval_question=self) \
            .order_by('priority')
        return qs























