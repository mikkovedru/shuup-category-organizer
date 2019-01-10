# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import shuup.apps


class AppConfig(shuup.apps.AppConfig):
    name = "shuup_category_organizer"
    verbose_name = "Shuup Category Organizer"
    label = "shuup_category_organizer"
    provides = {
        "admin_module": [
            "shuup_category_organizer.admin_module.CategoryOrganizerModule"
        ],
        "category_list_toolbar_provider": [
            "shuup_category_organizer.provider:AdminCategoryButtonProvider"
        ]
    }
