#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zzz_lib.zzz_log import zzz_print
from django.db import models
# from . import m_constants_mmr

# from django.apps import apps
# from django.conf import settings
# from django.core.exceptions import ObjectDoesNotExist

# ******************************************************************************
class meval_category(models.Model):
    display_text        = models.CharField      (max_length=100)
    url_text            = models.CharField      (max_length=16)
    created             = models.DateTimeField  (auto_now_add=True, help_text="timestamp of creation")
    updated             = models.DateTimeField  (auto_now=True, help_text="timestamp of last update")

    # --------------------------------------------------------------------------
    def __str__(self):
        return_string  = self.display_text
        return format(return_string)











