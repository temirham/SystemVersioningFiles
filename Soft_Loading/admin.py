from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from .models import *

admin.site.register([
    MainCategory, SubCategory, Platform, Soft, File,  Subscription, User
])

# @admin.register(Maincategories)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ("name", "view_main_cat_link")
#     def view_main_cat_link(self, obj):
#
#         count = obj.subcategories_set.count()
#         print(count)
#         url = (
#             reverse("admin:Soft_Loading__SubCategories_changelist")
#             + "?"
#             + urlencode({"MainCategories__main_cat_id": f"{obj.id}"})
#         )
#         return format_html('<a href="{}">{} Subcats</a>', url, count)
#     view_main_cat_link.short_description = "Main categories"
#
# @admin.register(Maincategories)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ("name", "main_cat_id_1")
#     def main_cat_id_1(self, obj):
#         count = obj..count()
#         url = (
#             reverse("admin:core_person_changelist")
#             + "?"
#             + urlencode({"courses__id": f"{obj.id}"})
#         )
#     main_cat_id_1.short_description =
#
# @admin.register(Subcategories)
# class PersonAdmin(admin.ModelAdmin):
#         search_fields = ("last_name__startswith",)


