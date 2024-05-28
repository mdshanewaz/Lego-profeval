#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zzz_lib.zzz_log import zzz_print

import copy
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect # , JsonResponse, Http404
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse

import os

from resumeweb.models import msendmail
from resumeweb.models import msendmail_failure

from resumeweb.views.vusergroup import test_is_superuser

from ..models import meval_category
from ..models import meval_module
from ..models import meval_question
from ..models import meval_reply
from ..models import meval_userscorerecommendation
from ..models import meval_useranswer
from ..models import mreferral_purchase

from resumeweb.models import mprod_eval
from resumeweb.models import mprod_eval_deliveryoption
from resumeweb.models import mprod_exp180
from resumeweb.models import mprod_exp180_deliveryoption
from resumeweb.models import mprod_exp180_serviceoption
from resumeweb.models import mcart
from resumeweb.models import mcart_deliveryoptions
from resumeweb.models import mcart_serviceoptions
from resumeweb.models import mcart_fileupload

from resumeweb.models import mcoupon

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_home"}))
def vdev_home(request):
    template    = loader.get_template('tdev/tbase_3columns_1footer.html')
    column_01   = column_02 = column_03 = footer_01 = ""
    title       = "vdev_home"
    viewname    = "vdev_home"
    # zzz_print("    %-28s: %s" % ("viewname", viewname))

    # --------------------------------------------------------------------------
    # Generate list of links to display
    url_list = []
    context = {'uv_view':'vdev_removedefaultdata', 'uv_params':'', 'uv_displaytext':'Remove Default Data'}
    url_list.append(render_to_string("tdev/tdev_columnchunk_linkurl.html", context))
    # --------------------------
    context = {'uv_view':'vdev_createdefaultdata', 'uv_params':'', 'uv_displaytext':'Create Default Data'}
    url_list.append(render_to_string("tdev/tdev_columnchunk_linkurl.html", context))
    # --------------------------
    context = {'uv_view':'vdev_sendtestemail', 'uv_params':'', 'uv_displaytext':'Send A Test Email To Dev'}
    url_list.append(render_to_string("tdev/tdev_columnchunk_linkurl.html", context))
    # --------------------------
    context = {'uv_view':'vdev_listfailedemails', 'uv_params':'', 'uv_displaytext':'List Emails That Failed To Send'}
    url_list.append(render_to_string("tdev/tdev_columnchunk_linkurl.html", context))
    # --------------------------
    context = {'uv_view':'vdev_displayenvbuildvariables', 'uv_params':'', 'uv_displaytext':'Display Build Variables'}
    url_list.append(render_to_string("tdev/tdev_columnchunk_linkurl.html", context))
    # --------------------------
    context = {'uv_view':'vdev_displaysettings', 'uv_params':'', 'uv_displaytext':'Display Settings Variables'}
    url_list.append(render_to_string("tdev/tdev_columnchunk_linkurl.html", context))
    # --------------------------
    context = {'uv_view':'vdev_logs', 'uv_params':'', 'uv_displaytext':'Display Logs'}
    url_list.append(render_to_string("tdev/tdev_columnchunk_linkurl.html", context))
    # --------------------------------------------------------------------------
    context = {'uv_view':'vdev_testingview', 'uv_params':'', 'uv_displaytext':'Development View For Testing Random Things'}
    url_list.append(render_to_string("tdev/tdev_columnchunk_linkurl.html", context))
    # --------------------------------------------------------------------------

    context   = {'generic_list':url_list, }
    column_01 = render_to_string("tdev/tdev_columnchunk_genericlist.html", context)

    context = {
        'column_01'                     : column_01,
        'column_02'                     : column_02,
        'column_03'                     : column_03,
        'footer_01'                     : footer_01,
        'title'                         : title,
        'viewname'                      : viewname,
        'templatename'                  : template.origin.__str__().rsplit('/', 1)[1],
    }
    return HttpResponse(template.render(context, request))

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_removedefaultdata"}))
def vdev_removedefaultdata(request):

    # mprod_eval data
    deleteTuple = mprod_eval.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mprod_eval DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = mprod_eval_deliveryoption.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mprod_eval_deliveryoption DELETED", deleteTuple[0], deleteTuple[1]))

    # mprod_exp180 data
    deleteTuple = mprod_exp180.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mprod_exp180 DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = mprod_exp180_deliveryoption.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mprod_exp180_deliveryoption DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = mprod_exp180_serviceoption.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mprod_exp180_serviceoption DELETED", deleteTuple[0], deleteTuple[1]))

    # mmr data
    deleteTuple = mreferral_purchase.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mreferral_purchase DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = meval_useranswer.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("meval_useranswer DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = meval_userscorerecommendation.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("meval_userscorerecommendation DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = meval_reply.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("meval_reply DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = meval_question.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("meval_question DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = meval_module.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("meval_module DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = meval_category.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("meval_category DELETED", deleteTuple[0], deleteTuple[1]))

    # mcart data
    deleteTuple = mcart_fileupload.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mcart_fileupload DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = mcart_deliveryoptions.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mcart_deliveryoptions DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = mcart_serviceoptions.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mcart_serviceoptions DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = mcart.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mcart DELETED", deleteTuple[0], deleteTuple[1]))

    deleteTuple = mcoupon.objects.all().delete()
    zzz_print("    %-40s: %3s   %s" % ("mcoupon DELETED", deleteTuple[0], deleteTuple[1]))

    return HttpResponseRedirect(reverse('vdev_home'))

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_createdefaultdata"}))
def vdev_createdefaultdata(request):

    # default meval setup
    qs = meval_category.objects.all()
    if qs.count():
        zzz_print("    %-28s: %s" % ("Skipping default meval setup", "meval_category_01 instances found"))
    else:
        # Ex: IT Position
        meval_category_01       = meval_category.objects.create  (display_text = "IT Position",     url_text="it_position")

        # Ex: IT Position: employment, education
        meval_module_0101       = meval_module.objects.create    (display_text = "Employment Module",     meval_category=meval_category_01,     priority=10,    url_text="employment")
        meval_module_0102       = meval_module.objects.create    (display_text = "Education Module",      meval_category=meval_category_01,     priority=20,    url_text="education")

        # Ex: questions for IT Position: employment
        meval_question_010101   = meval_question.objects.create  (display_text = "What is your employment status?", meval_module=meval_module_0101,       priority=10)
        meval_question_010102   = meval_question.objects.create  (display_text = "What is your employment history?", meval_module=meval_module_0101,       priority=20)

        # Ex: questions for IT Position: education
        meval_question_010201   = meval_question.objects.create  (display_text = "What level of university education do you have?", meval_module=meval_module_0102,       priority=10)
        meval_question_010202   = meval_question.objects.create  (display_text = "What education discipline were you in?", meval_module=meval_module_0102,       priority=20)

        # Ex: replies for IT Position: employment: question 01
        meval_reply_01010101    = meval_reply.objects.create  (display_text = "I am currently employed",     meval_question=meval_question_010101, priority=10,    score=10)
        meval_reply_01010102    = meval_reply.objects.create  (display_text = "I am NOT currently employed", meval_question=meval_question_010101, priority=20,    score=20)

        # Ex: replies for IT Position: employment: question 02
        meval_reply_01010201    = meval_reply.objects.create  (display_text = "I have no employment gap in the last year.",     meval_question=meval_question_010102, priority=10,    score=10)
        meval_reply_01010202    = meval_reply.objects.create  (display_text = "I have 2 month employment gap in the last year.",     meval_question=meval_question_010102, priority=20,    score=20)
        meval_reply_01010203    = meval_reply.objects.create  (display_text = "I have more than 2 month employment gap in the last year.",     meval_question=meval_question_010102, priority=30,    score=30)

        # Ex: replies for IT Position: education: question 01
        meval_reply_01020101    = meval_reply.objects.create  (display_text = "None",     meval_question=meval_question_010201, priority=10,    score=10)
        meval_reply_01020102    = meval_reply.objects.create  (display_text = "Undergraduate Degree",     meval_question=meval_question_010201, priority=20,    score=20)
        meval_reply_01020103    = meval_reply.objects.create  (display_text = "Graduate Degree",     meval_question=meval_question_010201, priority=30,    score=30)

        # Ex: replies for IT Position: education: question 02
        meval_reply_01020201    = meval_reply.objects.create  (display_text = "Arts",     meval_question=meval_question_010202, priority=10,    score=10)
        meval_reply_01020202    = meval_reply.objects.create  (display_text = "Science",     meval_question=meval_question_010202, priority=20,    score=20)
        meval_reply_01020203    = meval_reply.objects.create  (display_text = "Computer Science",     meval_question=meval_question_010202, priority=30,    score=30)

        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=10, score_low=10,  score_high=30,  display_text = "Recommendation 00",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=11, score_low=20,  score_high=40,  display_text = "Recommendation 01",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=12, score_low=30,  score_high=50,  display_text = "Recommendation 02",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=13, score_low=40,  score_high=60,  display_text = "Recommendation 03",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=14, score_low=50,  score_high=70,  display_text = "Recommendation 04",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=15, score_low=60,  score_high=80,  display_text = "Recommendation 05",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=16, score_low=70,  score_high=90,  display_text = "Recommendation 06",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=17, score_low=80,  score_high=100, display_text = "Recommendation 07",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=18, score_low=90,  score_high=110, display_text = "Recommendation 08",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=19, score_low=100, score_high=120, display_text = "Recommendation 09",)

        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=20, score_low=60,  score_high=70,  display_text = "Recommendation 10",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=21, score_low=60,  score_high=70,  display_text = "Recommendation 11",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=22, score_low=80,  score_high=90,  display_text = "Recommendation 12",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=23, score_low=80,  score_high=90,  display_text = "Recommendation 13",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=24, score_low=90,  score_high=100, display_text = "Recommendation 14",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=25, score_low=90,  score_high=100, display_text = "Recommendation 15",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=26, score_low=100, score_high=120, display_text = "Recommendation 16",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=27, score_low=100, score_high=110, display_text = "Recommendation 17",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=28, score_low=110, score_high=130, display_text = "Recommendation 18",)
        meval_usrec_01000000    = meval_userscorerecommendation.objects.create  (meval_category=meval_category_01, priority=29, score_low=100, score_high=120, display_text = "Recommendation 19",)

    # default mprod_eval setup
    qs = mprod_eval.objects.all()
    if qs.count():
        zzz_print("    %-28s: %s" % ("Skipping default mprod_eval setup", "mprod_eval instances found"))
    else:
        improd_eval_01 = mprod_eval.objects.create(meval_category=meval_category_01, listprice = 10, saleprice = 5.99, title = "IT CATEGORY ASSESSMENT", description = "description of IT CATEGORY ASSESSMENT")

        # mmh: commenting out delivery options for mprod_eval as they really don't need delivery options.
        # improd_eval_deliveryoption_01 = mprod_eval_deliveryoption.objects.create(name = "DO eval_all (72 hours)", listprice = 10, price = 10, hours_to_cancel_after_payment = 36, hours_to_deliver_after_payment = 72)
        # improd_eval_deliveryoption_01.products.add(improd_eval_01)
        #
        # improd_eval_deliveryoption_02 = mprod_eval_deliveryoption.objects.create(name = "DO eval_all (24 hours)", listprice = 27.50, price = 20, hours_to_cancel_after_payment = 12, hours_to_deliver_after_payment = 24)
        # improd_eval_deliveryoption_02.products.add(improd_eval_01)

    # default mprod_exp180 setup
    qs = mprod_exp180.objects.all()
    if qs.count():
        zzz_print("    %-28s: %s" % ("Skipping default mprod_exp180 setup", "mprod_exp180 instances found"))
    else:
        improd_exp180_01 = mprod_exp180.objects.create(listprice = 2.99, saleprice = 1.99, title = "P exp180_01", description = "description of p_exp180_01")
        improd_exp180_02 = mprod_exp180.objects.create(listprice = 3.99, saleprice = 2.99, title = "P exp180_02", description = "description of p_exp180_02")
        improd_exp180_03 = mprod_exp180.objects.create(listprice = 4.99, saleprice = 3.99, title = "P exp180_03", description = "description of p_exp180_03")

        improd_exp180_serviceoption_01_01 = mprod_exp180_serviceoption.objects.create(name = "SO exp180_01_01", products = improd_exp180_01, listprice = 10, price = 5)
        improd_exp180_serviceoption_01_02 = mprod_exp180_serviceoption.objects.create(name = "SO exp180_01_02", products = improd_exp180_01, listprice = 20, price = 15)
        improd_exp180_serviceoption_01_03 = mprod_exp180_serviceoption.objects.create(name = "SO exp180_01_03", products = improd_exp180_01, listprice = 5, price = 2)

        improd_exp180_serviceoption_02_01 = mprod_exp180_serviceoption.objects.create(name = "SO exp180_02_01", products = improd_exp180_02, listprice = 20, price = 1)
        improd_exp180_serviceoption_02_02 = mprod_exp180_serviceoption.objects.create(name = "SO exp180_02_02", products = improd_exp180_02, listprice = 40, price = 35)
        improd_exp180_serviceoption_02_03 = mprod_exp180_serviceoption.objects.create(name = "SO exp180_02_03", products = improd_exp180_02, listprice = 25, price = 12)
        improd_exp180_serviceoption_02_04 = mprod_exp180_serviceoption.objects.create(name = "SO exp180_02_04", products = improd_exp180_02, listprice = 125, price = 112)

        improd_exp180_deliveryoption_01 = mprod_exp180_deliveryoption.objects.create(name = "DO exp180_01_all (72 hours)", listprice = 10, price = 10, hours_to_cancel_after_payment = 36, hours_to_deliver_after_payment = 72)
        improd_exp180_deliveryoption_01.products.add(improd_exp180_01)
        improd_exp180_deliveryoption_01.products.add(improd_exp180_02)
        improd_exp180_deliveryoption_01.products.add(improd_exp180_03)

        improd_exp180_deliveryoption_02 = mprod_exp180_deliveryoption.objects.create(name = "DO exp180_02_all (48 hours)", listprice = 17.50, price = 17, hours_to_cancel_after_payment = 24, hours_to_deliver_after_payment = 48)
        improd_exp180_deliveryoption_02.products.add(improd_exp180_01)
        improd_exp180_deliveryoption_02.products.add(improd_exp180_02)
        improd_exp180_deliveryoption_02.products.add(improd_exp180_03)

        improd_exp180_deliveryoption_03 = mprod_exp180_deliveryoption.objects.create(name = "DO exp180_03_p01_only (24 hours)", listprice = 25, price = 20, hours_to_cancel_after_payment = 12, hours_to_deliver_after_payment = 24)
        improd_exp180_deliveryoption_03.products.add(improd_exp180_01)

        improd_exp180_deliveryoption_04 = mprod_exp180_deliveryoption.objects.create(name = "DO exp180_04_p02_only (24 hours)", listprice = 50, price = 45, hours_to_cancel_after_payment = 12, hours_to_deliver_after_payment = 24)
        improd_exp180_deliveryoption_04.products.add(improd_exp180_02)

        improd_exp180_deliveryoption_05 = mprod_exp180_deliveryoption.objects.create(name = "DO exp180_05_p02_only (24 hours)", listprice = 35, price = 30, hours_to_cancel_after_payment = 12, hours_to_deliver_after_payment = 24)
        improd_exp180_deliveryoption_05.products.add(improd_exp180_03)


    # default mcoupon setup
    qs = mcoupon.objects.all()
    if qs.count():
        zzz_print("    %-28s: %s" % ("Skipping default mcoupon setup", "mcoupon instances found"))
    else:
        imcoupon_01 = mcoupon.objects.create(category = "mprod_exp180", discount_percent = 25, hours_to_expire = 336, active = True)
        imcoupon_02 = mcoupon.objects.create(category = "mprod_exp180", discount_percent = 10, hours_to_expire = 336, active = True)
        imcoupon_03 = mcoupon.objects.create(category = "mprod_eval",   discount_percent = 25, hours_to_expire = 336, active = True)
        imcoupon_04 = mcoupon.objects.create(category = "mprod_eval",   discount_percent = 10, hours_to_expire = 336, active = True)

    return HttpResponseRedirect(reverse('vdev_home'))

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_sendtestemail"}))
def vdev_sendtestemail(request):
    viewname    = "vdev_sendtestemail"
    zzz_print("    %-28s: %s" % ("START", viewname))

    now = datetime.now()
    subject_text = "%s: Test Email Sent" % (now)

    to_emails_list = copy.deepcopy(settings.DEVELOPMENT_ONLY_EMAIL_RECIPIENTS)
    # zzz_print("    %-28s: %s" % ("to_emails_list", to_emails_list))

    plain_message_text  = subject_text
    html_message_text = plain_message_text
    imsendmail = msendmail.objects.add(
        subject             = subject_text,
        plain_message       = plain_message_text,
        html_message        = html_message_text,
        from_email          = settings.EMAIL_HOST_USER,
        to_emails_list      = to_emails_list
    )
    # imsendmail.send_to_entire_recipient_list()
    imsendmail.send_to_each_recipient_seperately()

    zzz_print("    %-28s: %s" % ("END", viewname))
    return HttpResponseRedirect(reverse('vdev_home'))

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_listfailedemails"}))
def vdev_listfailedemails(request):
    template    = loader.get_template('tdev/tbase_3columns_1footer.html')
    column_01   = column_02 = column_03 = footer_01 = ""
    title       = "vdev_listfailedemails"
    viewname    = "vdev_listfailedemails"
    # zzz_print("    %-28s: %s" % ("viewname", viewname))

    qs_unsent_emails = msendmail.objects.filter(sent_successfully=False)
    zzz_print("    %-28s: %s" % ("qs_unsent_emails.count()", qs_unsent_emails.count()))
    if qs_unsent_emails:
        context = {
            'qs'            : qs_unsent_emails,
        }
        column_01 = render_to_string("tdev/tdev_columnchunk_unsent_emails.html", context)

        context = {
            'uv_view'           : 'vdev_resendfailedemails',
            'uv_params'         : "",
            'uv_displaytext'    : "Try To Resend All Failed Emails"
        }
        footer_01 = render_to_string("tdev/tdev_columnchunk_linkurl.html", context)

    context = {
        'column_01'                     : column_01,
        'column_02'                     : column_02,
        'column_03'                     : column_03,
        'footer_01'                     : footer_01,
        'title'                         : title,
        'viewname'                      : viewname,
        'templatename'                  : template.origin.__str__().rsplit('/', 1)[1],
    }
    return HttpResponse(template.render(context, request))

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_resendfailedemails"}))
def vdev_resendfailedemails(request):
    # template    = loader.get_template('tdev/tbase_3columns_1footer.html')
    # # column_01   = column_02 = column_03 = footer_01 = ""
    # title       = "vdev_resendfailedemails"
    # viewname    = "vdev_resendfailedemails"
    # # zzz_print("    %-28s: %s" % ("viewname", viewname))

    # Get all unsent emails
    qs_unsent_emails = msendmail.objects.filter(sent_successfully=False)
    # zzz_print("    %-28s: %s" % ("qs_unsent_emails.count()", qs_unsent_emails.count()))

    # For each unsent email
    for unsent_email in qs_unsent_emails:
        # Get all sendmail_failures.
        # Doing this to retrieve their recipient_string.
        # Putting recipient_string in a list (final_recipients_list) which we later dict then list to remove duplicates.
        final_recipients_list = []
        for sendmail_failure in unsent_email.msendmail_failure_set.all():
            final_recipients_list.append(sendmail_failure.recipient_string)

        zzz_print("    %-28s: %s" % ("final_recipients_list BEFORE", final_recipients_list))
        # Remove duplicates from final_recipients_list
        final_recipients_list = list(dict.fromkeys(final_recipients_list))
        zzz_print("    %-28s: %s" % ("final_recipients_list AFTER", final_recipients_list))

        # Now actually try to re _send unsent_email with items in final_recipients_list
        for recipient_string in final_recipients_list:
            zzz_print("    %-28s: %s TO %s" % ("RESEND", unsent_email, recipient_string))
            unsent_email._send(recipient_string)

    return HttpResponseRedirect(reverse('vdev_listfailedemails'))

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_displayenvbuildvariables"}))
def vdev_displayenvbuildvariables(request):
    template    = loader.get_template('tdev/tbase_3columns_1footer.html')
    column_01   = column_02 = column_03 = footer_01 = ""
    title       = "vdev_displayenvbuildvariables"
    viewname    = "vdev_displayenvbuildvariables"
    # zzz_print("    %-28s: %s" % ("viewname", viewname))

    # for key, value in sorted(os.environ.items()):
    #     zzz_print("    %-28s: %s" % (key, value))

    context = {
        'generic_dict'              : dict(sorted(os.environ.items())),
    }
    column_01 = render_to_string("tdev/tdev_columnchunk_genericdict.html", context)

    context = {
        'column_01'                     : column_01,
        'column_02'                     : column_02,
        'column_03'                     : column_03,
        'footer_01'                     : footer_01,
        'title'                         : title,
        'viewname'                      : viewname,
        'templatename'                  : template.origin.__str__().rsplit('/', 1)[1],
    }
    return HttpResponse(template.render(context, request))


# ******************************************************************************
def view_chunk_column_01_file_links(filelist, current_filename=""):
    context = {
        'filelist'          : filelist,
        'current_filename'  : current_filename,
    }
    return render_to_string("tdev/tdev_column_01_file_links.html", context)

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_logs"}))
def vdev_logs(request, filename=""):
    template    = loader.get_template('tdev/tbase_3columns_1footer.html')
    column_01   = column_02 = column_03 = footer_01 = ""
    title       = "vdev_logs"
    viewname    = "vdev_logs"
    zzz_print("    %-28s: %s" % ("viewname", viewname))
    zzz_print("    %-28s: %s" % ("settings.LOG_DIRECTORY", settings.LOG_DIRECTORY))
    zzz_print("    %-28s: %s" % ("filename", filename))

    filelist = []
    with os.scandir(settings.LOG_DIRECTORY) as it:
        for entry in it:
            if entry.is_file():
                filelist.append(entry.name)

    working_filename = ""
    if filename:
        working_filename = settings.LOG_DIRECTORY + filename
    elif len(filelist):
        working_filename = settings.LOG_DIRECTORY + filelist[0]
    zzz_print("    %-28s: %s" % ("working_filename", working_filename))

    read_data = ""
    if working_filename:
        with open(working_filename) as f:
            read_data = f.read()
        read_data = read_data.replace('\n', '<br>')

    context = {
        'column_01'                     : view_chunk_column_01_file_links(sorted(filelist), current_filename=filename),
        'column_02'                     : read_data,
        'column_03'                     : column_03,
        'footer_01'                     : footer_01,
        'title'                         : title,
        'viewname'                      : viewname,
        'templatename'                  : template.origin.__str__().rsplit('/', 1)[1],
    }
    return HttpResponse(template.render(context, request))

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_displaysettings"}))
def vdev_displaysettings(request):
    template    = loader.get_template('tdev/tbase_3columns_1footer.html')
    column_01   = column_02 = column_03 = footer_01 = ""
    title       = "vdev_displaysettings"
    viewname    = "vdev_displaysettings"
    # zzz_print("    %-28s: %s" % ("viewname", viewname))

    # zzz_print("    %-28s: %s" % ("settings", settings))

    # for attr in dir(settings):
    #     print ("%-40s: %s" % (attr, getattr(settings, attr)))

    # get settings into dict
    settings_dict = settings.__dict__['_wrapped'].__dict__
    # for key, value in settings_dict.items():
        # zzz_print("    %-28s: %s" % (key, value))

    context = {
        'generic_dict'              : settings_dict,
    }
    column_01 = render_to_string("tdev/tdev_columnchunk_genericdict.html", context)

    context = {
        'column_01'                     : column_01,
        'column_02'                     : column_02,
        'column_03'                     : column_03,
        'footer_01'                     : footer_01,
        'title'                         : title,
        'viewname'                      : viewname,
        'templatename'                  : template.origin.__str__().rsplit('/', 1)[1],
    }
    return HttpResponse(template.render(context, request))

# ******************************************************************************
@user_passes_test(test_is_superuser, login_url=reverse_lazy("vug_failed_test", kwargs={'testname': "test_is_superuser", 'viewname': "vdev_testingview"}))
def vdev_testingview(request):
    viewname    = "vdev_testingview"
    zzz_print("    %-28s: %s" % ("viewname START", viewname))

    # # ?????????
    # # Question from Alex
    # dict1 = {'id': 161616, 'elements':[3333, '1']}
    # x = y = z = None
    # ch = {}
    #
    # for key, value in dict1.items():
    #     if key == "id":
    #         x = value
    #     elif key == "elements":
    #         y = value[0]
    #         z = value[1]
    # if x and y and z:
    #     ch['fnum'] = x
    #     ch['cNum'] = y
    #     ch['lv'] = z
    #
    # zzz_print("    %-28s: %s" % ("ch", ch))
    # ### ch : 'fnum': 161616, 'cNum': 3333, 'lv': '1'}
    #
    # # # Function Specification
    # # xml.etree.ElementTree.SubElement(parent, tag, attrib={}, **extra)
    # #
    # # # Alex's use
    # # sub1 = SubElement(root_elm, 'Car', ch)


    zzz_print("    %-28s: %s" % ("viewname END", viewname))
    return HttpResponseRedirect(reverse('vdev_home'))










































