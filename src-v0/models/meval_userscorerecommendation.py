#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zzz_lib.zzz_log import zzz_print
from django.db import models

# from django.core.exceptions import ObjectDoesNotExist
# from django.conf import settings
# from . import m_constants_mmr
# from django.apps import apps

# ******************************************************************************
class meval_userscorerecommendation(models.Model):
    display_text        = models.CharField      (max_length=100)
    priority            = models.IntegerField   ()
    score_low           = models.IntegerField   ()
    score_high          = models.IntegerField   ()
    meval_category      = models.ForeignKey     ('mmr.meval_category', on_delete=models.CASCADE)

    # --------------------------------------------------------------------------
    def __str__(self):
        return_string  = "meval_userscorerecommendation: " + str(self.id)
        return format(return_string)








