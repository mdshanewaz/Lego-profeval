# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# from django.contrib import admin

# from .models import meval_category
# from .models import meval_module
# from .models import meval_question
# from .models import meval_reply
# from .models import meval_userscorerecommendation


# @admin.register(meval_category)
# class Admin_meval_category(admin.ModelAdmin):
#     list_display = (
#         "display_text",
#         "url_text",
#     )
#     ordering = ('display_text',)

# @admin.register(meval_module)
# class Admin_meval_module(admin.ModelAdmin):
#     list_display = (
#         "meval_category",
#         "priority",
#         "display_text",
#         "url_text",
#     )
#     ordering = ('meval_category', 'priority', 'display_text')

# @admin.register(meval_question)
# class Admin_meval_question(admin.ModelAdmin):
#     list_display = (
#         "meval_module",
#         "priority",
#         "display_text",
#     )
#     ordering = ('meval_module', 'priority', 'display_text')

# @admin.register(meval_reply)
# class Admin_meval_reply(admin.ModelAdmin):
#     list_display = (
#         "meval_question",
#         "priority",
#         "score",
#         "display_text",
#     )
#     ordering = ('meval_question', 'priority', 'display_text')

# @admin.register(meval_userscorerecommendation)
# class Admin_meval_userscorerecommendation(admin.ModelAdmin):
#     list_display = (
#         "meval_category",
#         "priority",
#         "score_low",
#         "score_high",
#         "display_text",
#     )
#     ordering = ('meval_category', 'priority', 'display_text')


























