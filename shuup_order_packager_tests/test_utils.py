# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from shuup.testing.factories import create_product
from shuup_order_packager.utils import get_ordered_product_dimensions
from decimal import Decimal


@pytest.mark.django_db
def test_ordered_product_dimensions():
    p = create_product(sku='p1', width=100, depth=200, height=50)
    assert get_ordered_product_dimensions(p) == (Decimal(200), Decimal(100), Decimal(50))

    p = create_product(sku='p2', width=400, depth=900, height=500)
    assert get_ordered_product_dimensions(p) == (Decimal(900), Decimal(500), Decimal(400))
