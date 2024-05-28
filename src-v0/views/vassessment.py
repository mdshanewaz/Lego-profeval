#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zzz_lib.zzz_log import zzz_print

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Sum
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect # , JsonResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse

from ..models import meval_category
from ..models import meval_module
from ..models import meval_question #, form_meval_question
from ..models import meval_reply
from ..models import meval_useranswer
from ..models import meval_userscorerecommendation
from ..models import mreferral_purchase

import random

# from django.forms import modelformset_factory # formset_factory
# from django.forms import BaseModelFormSet
# from django.db import models

# from pprint import pprint
# from django.conf import settings
# from django.shortcuts import render
# import json

# ******************************************************************************
# While convenient this decorator duplicates queries that will be done in each view.
# Consider removing this and implementing something directly in each that uses this decorator.
def custom_assessment_view_decorator(view_function):
    def wrapper(request, *args, **kwargs):
        imreferral_purchase = mreferral_purchase.objects.get_valid_mreferral_purchase_for_user(request, kwargs['string_32'])

        if imreferral_purchase:
            # Test if link is still valid (i.e. time period has not passed)
            if not imreferral_purchase.link_still_valid():
                # zzz_print("    %-28s: %s" % ("imreferral_purchase.link_still_valid()", imreferral_purchase.link_still_valid()))

                # However only continue to expire this link if there are unanswered questions.
                # If all the questions have been answered this will evantually be redirected to recommendations view and therefor this link is valid and hasn't expired.
                qs_modulesWithoutAnswers = query_modules_without_answers_ordered_by_priority(imreferral_purchase)
                # zzz_print("    %-28s: %s" % ("qs_modulesWithoutAnswers.count()", qs_modulesWithoutAnswers.count()))
                if qs_modulesWithoutAnswers.count() > 0:
                    optionalmessage = "Referral_purchase: (" + kwargs['string_32'] + ") has expired."
                    failed_reverse_url = reverse_lazy("vug_failed_test", kwargs={'testname': "custom_assessment_view_decorator", 'viewname': view_function.__name__, 'optionalmessage': optionalmessage})
                    return redirect(failed_reverse_url)

            if 'module' not in kwargs:
                return view_function(request, *args, **kwargs)
            try:
                # zzz_print("    %-28s: %s" % ("'module' in kwargs", kwargs['module']))
                imeval_module = meval_module.objects.get(meval_category=imreferral_purchase.meval_category, url_text=kwargs['module'])
                return view_function(request, *args, **kwargs)
            except ObjectDoesNotExist:
                optionalmessage = "Referral_purchase: (" + kwargs['string_32'] + ") has invalid module (" + kwargs['module'] + ")"
                failed_reverse_url = reverse_lazy("vug_failed_test", kwargs={'testname': "custom_assessment_view_decorator", 'viewname': view_function.__name__, 'optionalmessage': optionalmessage})
                return redirect(failed_reverse_url)
        else:
            optionalmessage = "Invalid referral_purchase: (" + kwargs['string_32'] + ")"
            failed_reverse_url = reverse_lazy("vug_failed_test", kwargs={'testname': "custom_assessment_view_decorator", 'viewname': view_function.__name__, 'optionalmessage': optionalmessage})
            return redirect(failed_reverse_url)
    return wrapper

# ******************************************************************************
def query_modules_without_answers_ordered_by_priority(imreferral_purchase):
    qs = meval_module.objects \
        .filter(meval_category=imreferral_purchase.meval_category) \
        .annotate(num_answers=Count('meval_useranswer', filter=Q(meval_useranswer__mreferral_purchase=imreferral_purchase))) \
        .filter(num_answers__lte=0) \
        .order_by('priority')
    # zzz_print("    %-28s: %s" % ("query_modules_without_answers_ordered_by_priority", qs.count()))
    return qs

# ******************************************************************************
def query_modules_with_answers(imreferral_purchase):
    qs = meval_module.objects \
        .filter(meval_category=imreferral_purchase.meval_category) \
        .annotate(num_answers=Count('meval_useranswer', filter=Q(meval_useranswer__mreferral_purchase=imreferral_purchase))) \
        .filter(num_answers__gt=0)
    # zzz_print("    %-28s: %s" % ("query_modules_with_answers", qs.count()))
    return qs

# ******************************************************************************
@custom_assessment_view_decorator
def vassessment_terms(request, string_32):
    title    = "vassessment_terms"
    viewname = "vassessment_terms"
    zzz_print("    %-28s: %s" % ("VIEW", viewname))
    zzz_print("    %-28s: %s" % ("string_32", string_32))

    imreferral_purchase = mreferral_purchase.objects.get_valid_mreferral_purchase_for_user(request, string_32)
    template = loader.get_template('mmr_v2/layout/terms.html')
    context = {
        'string_32'                     : string_32,
        'title'                         : title,
        'viewname'                      : viewname,
        'templatename'                  : template.origin.__str__().rsplit('/', 1)[1],
    }
    return HttpResponse(template.render(context, request))

# ******************************************************************************
@custom_assessment_view_decorator
def vassessment_terms_accepted(request, string_32):
    title    = "vassessment_terms_accepted"
    viewname = "vassessment_terms_accepted"
    zzz_print("    %-28s: %s" % ("VIEW", viewname))
    zzz_print("    %-28s: %s" % ("string_32", string_32))

    # Set terms_accepted for imreferral_purchase
    imreferral_purchase = mreferral_purchase.objects.get_valid_mreferral_purchase_for_user(request, string_32)
    imreferral_purchase.terms_accepted = True
    imreferral_purchase.save()

    # and redirect back to vassessment_home
    # return HttpResponseRedirect(reverse('vassessment_home', kwargs={'string_32':string_32}))
    hack_param = random.randint(10000,99999)
    zzz_print("    %-28s: %s" % ("hack_param", hack_param))
    return HttpResponseRedirect(reverse('vassessment_home_with_hack_param', kwargs={'string_32':string_32,'hack_param':hack_param}))

# ******************************************************************************
def view_chunk_column_02_module_question_reply__v2_as_form(request, imreferral_purchase, imeval_module):
    # zzz_print("    %-28s: %s" % ("view_chunk_column_02_module_question_reply__v2_as_form", ""))
    # zzz_print("    %-28s: %s" % ("imreferral_purchase", imreferral_purchase))
    # zzz_print("    %-28s: %s" % ("imeval_module", imeval_module))

    # # Get all previous answers for this purchase, as a list
    # all_answer_ids_list = meval_useranswer.objects.filter(mreferral_purchase=imreferral_purchase).values_list('meval_reply_id', flat=True)
    # all_answer_ids_list = list(all_answer_ids_list)     # convert to list
    # # zzz_print("    %-28s: %s" % ("all_answer_ids_list", all_answer_ids_list))

    # Get qs of all questions for this moddule
    qs = meval_question.objects.filter(meval_module=imeval_module).order_by('priority')
    # zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))

    # Generate new_fields_dict which will be used to create the DynamicForm.
    # Each field represents one form field.
    # The label is modified manually to be the question text. Otherwise it would be the question id.
    new_fields_dict = {}
    for imeval_question in qs:
        qs2 = meval_reply.objects.filter(meval_question=imeval_question).order_by('priority')

        # # ----------------------------------------------------------------------------------------------
        # # # BASED ON A QUERY TO meval_useranswer I NEED TO SET A CHECKED VALUE FOR THE PROPER
        # # # ITEM IN ModelChoiceField OPTIONS.
        # # new_field.checked = True
        # initial_dict = {}
        # for item in qs2:
        #     if item.id in all_answer_ids_list:
        #         # zzz_print("    %-28s: %s" % ("SOMEHOW FORCE THIS OPTION CHECKED", item))
        #         # initial_dict = {'id', item.id}
        #         # initial_dict = {'id': item.id}
        #         initial_dict['id'] = item.id
        #         break
        # # zzz_print("    %-28s: %s" % ("initial_dict", initial_dict))
        # # ----------------------------------------------------------------------------------------------

        new_field = forms.ModelChoiceField(
        # new_field = ModelChoiceField_withDifferentLabel(
                                    queryset        = qs2,
                                    widget          = forms.RadioSelect,
                                    # to_field_name   = 'display_text',
                                    # initial         = initial_dict,
                                    # empty_label     = None
                                    )
        # zzz_print("    %-28s: %s" % ("new_field", new_field))
        # zzz_print("    %-28s: %s" % ("new_field.initial", new_field.initial))

        # choices = new_field._get_choices()
        # for choice in choices:
        #     zzz_print("    %-28s: %s" % ("choice", choice))
        #     zzz_print("    %-28s: %s" % ("choice[0]", choice[0]))
        #     zzz_print("    %-28s: %s" % ("choice[1]", choice[1]))
        #     if choice[0] in all_answer_ids_list:
        #         choice[1].checked = True

        # change label
        new_field.label = imeval_question.display_text  + " ( id = " + str(imeval_question.id) + ")"
        # Add new_field to new_fields_dict
        new_fields_dict[str(imeval_question.id)] = new_field

    # # NOTE; python type call to create a new object MODIFIES the third DICT parameter!
    # for key in new_fields_dict.items():
    #     zzz_print("    %-28s: %s" % ("key A:", key))

    # NOTE; python type call to create a new object MODIFIES the third DICT parameter!
    # Actually create the dynamic form based from forms.Form using the dict above
    DynamicForm = type('DynamicForm', (forms.Form,), new_fields_dict)

    # # NOTE; python type call to create a new object MODIFIES the third DICT parameter!
    # for key in new_fields_dict.items():
    #     zzz_print("    %-28s: %s" % ("key B:", key))
    # NOTE; python type call to create a new object MODIFIES the third DICT parameter!
    # for key, value in new_fields_dict['declared_fields'].items():
    #     zzz_print("    %-28s: %s" % ("key C:", key))
    #     zzz_print("    %-28s: %s" % ("value C:", value))
    #     # value.label = "blue"


    # zzz_print("    %-28s: %s" % ("------------------------------------", ""))
    # pprint(DynamicForm)
    # zzz_print("    %-28s: %s" % ("------------------------------------", ""))

    if request.method == 'POST':
        form = DynamicForm(request.POST)
        if form.is_valid():
            # zzz_print("    %-28s: %s" % ("form.is valid()", ""))

            # NOTE; python type call to create a new object MODIFIES the third DICT parameter!
            for imeval_question_id in new_fields_dict['declared_fields']:
                # zzz_print("    %-28s: %s" % ("imeval_question_id declared_fields", imeval_question_id))
                imeval_reply = form.cleaned_data.get(imeval_question_id)
                # zzz_print("    question_id %-16s: imeval_reply = %s" % (imeval_question_id, imeval_reply))

                # save users answer to database
                imeval_useranswer = meval_useranswer.objects.add_or_update(
                    mreferral_purchase  = imreferral_purchase,
                    mmeval_module       = imeval_module,
                    meval_question_id   = imeval_question_id,
                    meval_reply         = imeval_reply,
                )

            # This EMPTY return Will force a
            # HttpResponseRedirect(reverse('vassessment_home', kwargs={'string_32':string_32}))
            return
        else:
            zzz_print("    %-28s: %s" % ("form.is NOT valid()", ""))
    else:
        form = DynamicForm()
        # form = DynamicForm(initial=initial_dict)

    # # Version 1
    # form_html = render_to_string('mmr_v1/tform.html', {'form':form}, request=request)
    # Version 2
    form_html = render_to_string('mmr_v2/pg-contents/tform.html', {'form':form}, request=request)

    # zzz_print("    %-28s: %s" % ("form_html", form_html))
    return form_html

# ******************************************************************************
@custom_assessment_view_decorator
def vassessment_home(request, string_32, hack_param=None):
    title    = "vassessment_home"
    viewname = "vassessment_home"
    zzz_print("    %-28s: %s" % ("VIEW", viewname))
    zzz_print("    %-28s: %s" % ("string_32", string_32))
    zzz_print("    %-28s: %s" % ("hack_param", hack_param))

    imreferral_purchase = mreferral_purchase.objects.get_valid_mreferral_purchase_for_user(request, string_32)
    if not imreferral_purchase.terms_accepted:
        zzz_print("    %-28s: %s" % ("vassessment_home", "TERMS NOT YET ACCEPTED"))
        return HttpResponseRedirect(reverse('vassessment_terms', kwargs={'string_32':string_32}))

    qs_modulesWithoutAnswers = query_modules_without_answers_ordered_by_priority(imreferral_purchase)
    if qs_modulesWithoutAnswers.count() == 0:
        zzz_print("    %-28s: %s" % ("vassessment_home", "QUESTIONS NOT PENDING"))
        return HttpResponseRedirect(reverse('vassessment_recommendations', kwargs={'string_32':string_32}))

    qs_modulesWithAnswers   = query_modules_with_answers(imreferral_purchase)
    total_modules           = qs_modulesWithoutAnswers.count() + qs_modulesWithAnswers.count()
    modules_answered        = qs_modulesWithAnswers.count()
    imeval_module           = qs_modulesWithoutAnswers[0]
    form_html               = view_chunk_column_02_module_question_reply__v2_as_form(request, imreferral_purchase, imeval_module)

    # If form_html is empty that means the form successfully processed and so redirect
    if not form_html:
        zzz_print("    %-28s: %s" % ("form_html is empty", "Form must have processed successfully. Redirecting to vassessment_home"))
        return HttpResponseRedirect(reverse('vassessment_home', kwargs={'string_32':string_32}))

    template = loader.get_template('mmr_v2/layout/qa_page.html')
    context = {
        'imreferral_purchase'           : imreferral_purchase,
        'total_modules'                 : total_modules,
        'modules_answered'              : modules_answered,
        'imeval_module'                 : imeval_module,
        'form_html'                     : form_html,
        'title'                         : title,
        'viewname'                      : viewname,
        'templatename'                  : template.origin.__str__().rsplit('/', 1)[1],
    }
    return HttpResponse(template.render(context, request))

# ******************************************************************************
@custom_assessment_view_decorator
def vassessment_recommendations(request, string_32):
    title    = "vassessment_recommendations"
    viewname = "vassessment_recommendations"
    zzz_print("    %-28s: %s" % ("VIEW", viewname))
    zzz_print("    %-28s: %s" % ("string_32", string_32))

    imreferral_purchase = mreferral_purchase.objects.get_valid_mreferral_purchase_for_user(request, string_32)
    if not imreferral_purchase.terms_accepted:
        return HttpResponseRedirect(reverse('vassessment_terms', kwargs={'string_32':string_32}))

    qs_modulesWithAnswers = query_modules_with_answers(imreferral_purchase)
    if qs_modulesWithAnswers.count() == 0:
        zzz_print("    %-28s: %s" % ("vassessment_recommendations", "QUESTIONS STILL PENDING"))
        return HttpResponseRedirect(reverse('vassessment_home', kwargs={'string_32':string_32}))

    users_score_aggregate = meval_useranswer.objects \
        .filter(mreferral_purchase=imreferral_purchase) \
        .aggregate(Sum('meval_reply__score'))

    zzz_print("    %-28s: %s" % ("users_score_aggregate", users_score_aggregate))
    zzz_print("    %-28s: %s" % ("users_score_aggregate[meval_reply__score__sum]", users_score_aggregate['meval_reply__score__sum']))

    users_score = users_score_aggregate['meval_reply__score__sum']

    qs = meval_userscorerecommendation.objects \
        .filter(meval_category=imreferral_purchase.meval_category) \
        .filter(score_low__lte=users_score) \
        .filter(score_high__gte=users_score) \
        .order_by('priority')
    zzz_print("    %-28s: %s" % ("qs.count()", qs.count()))

    template = loader.get_template('mmr_v2/layout/qa_recommendations.html')
    context = {
        'qs'                        : qs,
        'users_score'               : users_score,
        'imreferral_purchase'       : imreferral_purchase,
        'title'                     : title,
        'viewname'                  : viewname,
        'templatename'              : template.origin.__str__().rsplit('/', 1)[1],
    }
    return HttpResponse(template.render(context, request))


















