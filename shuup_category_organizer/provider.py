# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from shuup.admin.toolbar import BaseToolbarButtonProvider, URLActionButton


class AdminCategoryButtonProvider(BaseToolbarButtonProvider):
    @classmethod
    def get_buttons_for_view(cls, view):
        return [
            URLActionButton(
                url=reverse("shuup_admin:category.organize"),
                text=_("Organize"),
                tooltip=_("Organize categories"),
                icon="fa fa-sitemap",
                extra_css_class="btn-default btn-organize-categories"
            )
        ]
