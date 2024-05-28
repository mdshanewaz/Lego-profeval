#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zzz_lib.zzz_log import zzz_print

from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from resumeweb.models.muniqueid import muniqueid_get_users_uniquid

from . import m_constants_mmr

# from django.apps import apps

# ******************************************************************************
class mreferral_purchase_instancemanager(models.Manager):
    # --------------------------------------------------------------------------
    def mreferral_purchase_add(self, request, meval_category):
        owner_uniqid        = muniqueid_get_users_uniquid(request)
        random_string_32    = get_random_string(length=32)
        # zzz_print("    %-28s: %s" % ("mreferral_purchase_add", ""))
        # zzz_print("    %-28s: %s" % ("owner_uniqid", owner_uniqid))
        # zzz_print("    %-28s: %s" % ("random_string_32", random_string_32))

        mreferral_purchase_instance = self.create(owner_uniqid=owner_uniqid, meval_category=meval_category, random_string_32=random_string_32)
        if request.user.is_authenticated:
            # zzz_print("    %-28s: %s" % ("*** request.user.is_authenticated", "TRUE"))
            mreferral_purchase_instance.muser = request.user
            mreferral_purchase_instance.save()
        return mreferral_purchase_instance

    # --------------------------------------------------------------------------
    def get_valid_mreferral_purchase_for_user(self, request, string_32):
        owner_uniqid = muniqueid_get_users_uniquid(request)
        # zzz_print("    %-28s: %s" % ("get_valid_mreferral_purchase_for_user", ""))
        # zzz_print("    %-28s: %s" % ("owner_uniqid", owner_uniqid))
        # zzz_print("    %-28s: %s" % ("string_32", string_32))

        try:
            imreferral_purchase = mreferral_purchase.objects.get(owner_uniqid=owner_uniqid, random_string_32=string_32)
            # zzz_print("    %-28s: %s" % ("get_valid_mreferral_purchase_for_user", "True by owner_uniqid"))
            return imreferral_purchase
        except ObjectDoesNotExist:
            if request.user.is_authenticated:
                try:
                    imreferral_purchase = mreferral_purchase.objects.get(muser=request.user, random_string_32=string_32)
                    # zzz_print("    %-28s: %s" % ("get_valid_mreferral_purchase_for_user", "True by muser"))
                    return imreferral_purchase
                except ObjectDoesNotExist:
                    zzz_print("    %-28s: %s" % ("get_valid_mreferral_purchase_for_user", "False by muser"))
                    return None
            else:
                zzz_print("    %-28s: %s" % ("get_valid_mreferral_purchase_for_user", "False for guest muser"))
                return None

# ******************************************************************************
class mreferral_purchase(models.Model):
    objects             = mreferral_purchase_instancemanager()
    owner_uniqid        = models.CharField      (max_length=100)
    muser               = models.ForeignKey     (settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    meval_category      = models.ForeignKey     ('mmr.meval_category', on_delete=models.CASCADE)
    random_string_32    = models.CharField      (max_length=33)
    terms_accepted      = models.BooleanField   (default=False)
    created             = models.DateTimeField  (auto_now_add=True, help_text="timestamp of creation")

    # --------------------------------------------------------------------------
    def __str__(self):
        return_string  = self.random_string_32 + ", " + self.meval_category.display_text
        return format(return_string)

    # --------------------------------------------------------------------------
    def get_link_to_assessment(self):
        link_url = settings.DNS_NAME + reverse("vassessment_home", kwargs={'string_32': self.random_string_32})
        # zzz_print("    %-28s: %s" % ("link_url", link_url))
        return format(link_url)

    # --------------------------------------------------------------------------
    def link_still_valid(self):
        # zzz_print("    %-28s: %s" % ("link_still_valid", ""))
        now = timezone.now()  # using django timezone

        TD_since_purchase   = now - self.created
        # TD_valid_until   = timedelta(hours=self.mcart_deliveryoptions.hours_to_cancel_after_payment)
        TD_valid_until      = timedelta(days=m_constants_mmr.CONST_MEVAL_LINK_IS_VALID_FOR_THIS_NUMBER_OF_DAYS_AFTER_PURCHASE)
        TD_valid_left       = TD_valid_until - TD_since_purchase
        if TD_valid_left < timedelta(hours=0):
            return False
        return True

