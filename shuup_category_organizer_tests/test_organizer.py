# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import json

import pytest
from django.core.urlresolvers import reverse
from django.test import Client
from shuup.admin.modules.categories.views.list import CategoryListView
from shuup.core.models import Category
from shuup.testing import factories
from shuup.testing.utils import apply_request_middleware

from shuup_category_organizer.admin_module.views import CategoryOrganizeView


@pytest.mark.django_db
def test_category_organize_view(rf, admin_user):
    shop = factories.get_default_shop()

    cat1 = Category.objects.create(name="cat1")
    cat2 = Category.objects.create(name="cat2")
    cat3 = Category.objects.create(name="cat3")

    cat1.shops.add(shop)
    cat2.shops.add(shop)
    cat3.shops.add(shop)

    view = CategoryOrganizeView.as_view()
    request = apply_request_middleware(rf.get("/"), user=admin_user)
    response = view(request)
    assert response.status_code == 200
    response.render()
    content = response.content.decode("utf-8")
    assert "Organize categories" in content

    payload = [
        {
            "id": cat1.pk,
            "visible_in_menu": True,
            "position": 1,
            "children": [
                {
                    "id": cat2.pk,
                    "visible_in_menu": False,
                    "position": 1
                },
                {
                    "id": cat3.pk,
                    "visible_in_menu": True,
                    "position": 2
                }
            ]
        }
    ]
    # do nothing..
    request = apply_request_middleware(rf.post("/"), user=admin_user)
    response = view(request)
    assert response.status_code == 200
    cat1 = Category.objects.get(pk=cat1.pk)
    cat2 = Category.objects.get(pk=cat2.pk)
    cat3 = Category.objects.get(pk=cat3.pk)
    assert cat1.parent is None
    assert cat2.parent is None
    assert cat3.parent is None

    request = apply_request_middleware(rf.post("/", data={"payload": json.dumps(payload)}), user=admin_user)
    response = view(request)
    assert response.status_code == 200

    cat1 = Category.objects.get(pk=cat1.pk)
    cat2 = Category.objects.get(pk=cat2.pk)
    cat3 = Category.objects.get(pk=cat3.pk)
    assert cat1.parent is None
    assert cat2.parent == cat1
    assert cat3.parent == cat1


@pytest.mark.django_db
def test_organizer_button(rf, admin_user):
    factories.get_default_shop()
    view = CategoryListView.as_view()
    request = apply_request_middleware(rf.get("/"), user=admin_user)
    response = view(request)
    assert response.status_code == 200
    response.render()
    content = response.content.decode("utf-8")
    assert "btn-organize-categories" in content


@pytest.mark.django_db
def test_duplicate_view(admin_user):
    shop = factories.get_default_shop()
    category = factories.get_default_category()
    category.shops.add(shop)

    client = Client()
    client.login(username=admin_user.username, password="password")

    duplicate_url = reverse("shuup_admin:category.duplicate", kwargs=dict(pk=category.pk))
    response = client.post(duplicate_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
    assert response.status_code == 200

    duplicate_url = reverse("shuup_admin:category.duplicate", kwargs=dict(pk=999))
    response = client.post(duplicate_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
    assert response.status_code == 404
