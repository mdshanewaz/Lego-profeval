#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zzz_lib.zzz_log import zzz_print
from django.db import models
# from . import m_constants_mmr

# from django.apps import apps
# from django.conf import settings
# from django.core.exceptions import ObjectDoesNotExist

# ******************************************************************************
class meval_module(models.Model):
    display_text        = models.CharField      (max_length=100)
    url_text            = models.CharField      (max_length=16)
    meval_category      = models.ForeignKey     ('mmr.meval_category', on_delete=models.CASCADE)
    priority            = models.IntegerField   ()

    # --------------------------------------------------------------------------
    def __str__(self):
        # return_string  = self.meval_category.display_text + "_" + self.display_text
        return_string  = self.display_text
        return format(return_string)











