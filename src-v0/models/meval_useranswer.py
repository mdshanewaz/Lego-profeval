#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zzz_lib.zzz_log import zzz_print
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# from django.conf import settings
# from . import m_constants_mmr
# from django.apps import apps


# ******************************************************************************
class meval_useranswer_instancemanager(models.Manager):
    # --------------------------------------------------------------------------
    def add_or_update(self, mreferral_purchase, mmeval_module, meval_question_id, meval_reply):
        add_or_update_mode = "EXISTS"
        bool_updated_existing = False
        try:
            meval_useranswer_instance = meval_useranswer.objects.get(mreferral_purchase=mreferral_purchase, mmeval_module=mmeval_module, meval_question_id=meval_question_id)
            if meval_useranswer_instance.meval_reply != meval_reply:
                meval_useranswer_instance.meval_reply = meval_reply
                meval_useranswer_instance.save()
                bool_updated_existing = True

        except ObjectDoesNotExist:
            add_or_update_mode = "ADDED"
            meval_useranswer_instance = self.create(mreferral_purchase=mreferral_purchase, mmeval_module=mmeval_module, meval_question_id=meval_question_id, meval_reply=meval_reply)
        zzz_print("    %-28s: %s, %s" % ("add_or_update", add_or_update_mode, meval_useranswer_instance.__str__()))
        if bool_updated_existing:
            zzz_print("    %-28s: %s" % ("EXISTING ENTRY UPDATED TO", meval_useranswer_instance.meval_reply))

# ******************************************************************************
class meval_useranswer(models.Model):
    objects             = meval_useranswer_instancemanager()
    mreferral_purchase  = models.ForeignKey     ('mmr.mreferral_purchase', on_delete=models.CASCADE)
    mmeval_module       = models.ForeignKey     ('mmr.meval_module', on_delete=models.CASCADE)
    meval_question_id   = models.IntegerField   ()
    meval_reply         = models.ForeignKey     ('mmr.meval_reply', on_delete=models.CASCADE)
    created             = models.DateTimeField  (auto_now_add=True, help_text="timestamp of creation")
    updated             = models.DateTimeField  (auto_now=True, help_text="timestamp of last update")

    # --------------------------------------------------------------------------
    def __str__(self):
        return_string  = "meval_useranswer: " + str(self.id)
        return format(return_string)

    # --------------------------------------------------------------------------
    class Meta:
        unique_together = ('mreferral_purchase', 'meval_question_id', )








