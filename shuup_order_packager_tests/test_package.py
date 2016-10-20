# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shuup_order_packager.package.simple import SimplePackage
import pytest
from shuup.testing.factories import create_product
from shuup_order_packager.utils import get_ordered_product_dimensions


def test_simple_package():
    base_pkge = SimplePackage()
    assert base_pkge.width == 0
    assert base_pkge.count == 0
    assert base_pkge.height == 0
    assert base_pkge.length == 0
    assert base_pkge.weight == 0
    assert base_pkge.volume == 0

    repr(base_pkge)


@pytest.mark.django_db
def test_add_product():
    product1 = create_product(sku='p1', width=100, depth=200, height=50, gross_weight=2340)

    p1_width, p1_length, p1_height = get_ordered_product_dimensions(product1)

    pkge = SimplePackage()
    repr(pkge)
    assert pkge.count == 0
    assert pkge.volume == 0

    # adiciona o produto uma vez
    pkge.add_product(product1)
    assert pkge.width == p1_width
    assert pkge.height == p1_height
    assert pkge.length == p1_length
    assert pkge.weight == product1.gross_weight
    assert pkge.count == 1
    assert pkge.volume == (p1_width * p1_length * p1_height)

    # adiciona o produto outra vez
    pkge.add_product(product1)
    assert pkge.width == p1_width
    assert pkge.length == p1_length
    assert pkge.height == p1_height * 2
    assert pkge.weight == product1.gross_weight * 2
    assert pkge.count == 2
    assert pkge.volume == (p1_width * p1_length * (p1_height * 2))

    repr(pkge)

    # cria um produto novo
    product2 = create_product(sku='p2', width=168, depth=365, height=50, gross_weight=1204)
    p2_width, p2_length, p2_height = get_ordered_product_dimensions(product2)

    # adiciona o novo
    pkge.add_product(product2)
    assert pkge.width == max(p1_width, p2_width)
    assert pkge.length == max(p1_length, p2_length)
    assert pkge.height == p1_height * 2 + p2_height
    assert pkge.weight == product1.gross_weight * 2 + product2.gross_weight
    assert pkge.count == 3
    assert pkge.volume == max(p1_width, p2_width) * max(p1_length, p2_length) * (p1_height * 2 + p2_height)
