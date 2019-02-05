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
from shuup.admin.utils.urls import admin_url


class CategoryOrganizerModule(AdminModule):
    name = _("Category Organizer")
    category = _("Category Organizer")
    breadcrumbs_menu_entry = MenuEntry(text=name, url="shuup_admin:category.list", category=PRODUCTS_MENU_CATEGORY)

    def get_urls(self):
        return [
            admin_url(
                r"^categories/organize/$",
                "shuup_category_organizer.admin_module.views.CategoryOrganizeView",
                name="category.organize"
            ),
            admin_url(
                r"^categories/(?P<pk>\d+)/duplicate/$",
                "shuup_category_organizer.admin_module.views.CategoryDuplicateView",
                name="category.duplicate"
            )
        ]
