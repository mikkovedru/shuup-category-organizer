# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.utils.translation import ugettext_lazy as _
from shuup.admin.base import AdminModule, MenuEntry
from shuup.admin.menu import PRODUCTS_MENU_CATEGORY
from shuup.admin.utils.permissions import get_default_model_permissions
from shuup.admin.utils.urls import admin_url
from shuup.core.models import Category


class CategoryOrganizerModule(AdminModule):
    name = _("Categories")
    category = _("Categories")
    breadcrumbs_menu_entry = MenuEntry(text=name, url="shuup_admin:category.list", category=PRODUCTS_MENU_CATEGORY)

    def get_urls(self):
        return [
            admin_url(
                r"^categories/organize/$",
                "shuup_category_organizer.admin_module.views.CategoryOrganizeView",
                name="category.organize",
                permissions=get_default_model_permissions(Category)
            ),
            admin_url(
                r"^categories/(?P<pk>\d+)/duplicate/$",
                "shuup_category_organizer.admin_module.views.CategoryDuplicateView",
                name="category.duplicate",
                permissions=get_default_model_permissions(Category)
            )
        ]

    def get_required_permissions(self):
        return get_default_model_permissions(Category)
