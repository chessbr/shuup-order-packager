# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from shuup_order_packager.constraints.simple import WeightPackageConstraint,\
    SimplePackageDimensionConstraint
from shuup.testing.factories import create_product, get_default_shop,\
    get_default_supplier
from shuup_order_packager.algorithms.simple import SimplePackager
from shuup.testing.utils import apply_request_middleware
from shuup.front.basket import get_basket, get_basket_order_creator
from shuup.core.models._orders import OrderStatus
from shuup.testing.mock_population import populate_if_required


@pytest.mark.django_db
def test_simple_packager1(rf):
    populate_if_required()
    MAX_WIDTH = 1050
    MAX_LENGTH = 1050
    MAX_HEIGHT = 1050
    MAX_EDGES_SUM = 2000
    MAX_WEIGHT = 30000

    constraint1 = SimplePackageDimensionConstraint(MAX_WIDTH, MAX_LENGTH, MAX_HEIGHT, MAX_EDGES_SUM)
    constraint2 = WeightPackageConstraint(MAX_WEIGHT)

    packager = SimplePackager()
    assert packager._constraints == set()
    packager.add_constraint(constraint1)
    packager.add_constraint(constraint2)
    assert constraint1 in packager._constraints
    assert constraint2 in packager._constraints

    product1 = create_product(sku='p1', width=250, depth=200, height=50, gross_weight=2340,
                              shop=get_default_shop(), supplier=get_default_supplier())

    product2 = create_product(sku='p2', width=500, depth=150, height=90, gross_weight=690,
                              shop=get_default_shop(), supplier=get_default_supplier())

    assert packager._product_has_valid_attrs(product1) is True
    assert packager._product_has_valid_attrs(product2) is True

    # cria produtos invalidos, sem propriedades necessárias

    # no gross_weight
    product_invalid_1 = create_product(sku='pi1', width=100, depth=200, height=50, gross_weight=100)
    product_invalid_1.gross_weight = 0
    assert packager._product_has_valid_attrs(product_invalid_1) is False

    # no height
    product_invalid_2 = create_product(sku='pi2', width=100, depth=200, height=50, gross_weight=100)
    product_invalid_2.height = 0
    assert packager._product_has_valid_attrs(product_invalid_2) is False

    # no depth
    product_invalid_3 = create_product(sku='pi3', width=100, depth=200, height=50, gross_weight=100)
    product_invalid_3.depth = 0
    assert packager._product_has_valid_attrs(product_invalid_3) is False

    # no width
    product_invalid_4 = create_product(sku='pi4', width=100, depth=200, height=50, gross_weight=100)
    product_invalid_4.width = 0
    assert packager._product_has_valid_attrs(product_invalid_4) is False


    # cria um basket vazio
    request = rf.get("/")
    request.session = {}
    request.shop = get_default_shop()
    apply_request_middleware(request)
    basket = get_basket(request)

    # adiciona um item no carrinho
    basket.add_product(supplier=get_default_supplier(),
                       shop=get_default_shop(),
                       product=product1, quantity=2)

    basket.add_product(supplier=get_default_supplier(),
                       shop=get_default_shop(),
                       product=product2, quantity=3)

    # cria o pedido a partir do carrinho
    order_creator = get_basket_order_creator()
    basket.status = OrderStatus.objects.get_default_initial()
    order = order_creator.create_order(basket)

    packages_from_source = packager.pack_source(basket)
    packages_from_order = packager.pack_order(order)

    # os produtos cabem todos no mesmo pacote
    assert len(packages_from_source) == 1
    assert len(packages_from_order) == 1

    pkge_from_source = packages_from_source[0]
    pkge_from_order = packages_from_order[0]

    for pkge in (pkge_from_source, pkge_from_order):
        assert pkge.count == 5     # 5 produtos
        assert pkge.weight == (product1.gross_weight*2 + product2.gross_weight*3)  # peso igual
        assert pkge.width == 500       # product2 width
        assert pkge.length == 200      # product1 depth
        assert pkge.height == (product1.height*2 + product2.height*3)  # soma as alturas


@pytest.mark.django_db
def test_simple_packager_several_packages():
    """
    In this test, we will pack 15 units of a same product.
    The result must be several packages.

    The package maximum size will be 105cm x 105cm x 105cm and the
    package edges sum can not sum 200cm.
    The maximum weight is 30kg.

    The product size is 34cm x 32cm x 18cm and it's weight is 7.7kg
    """
    MAX_WIDTH = 1050        # 1.05m
    MAX_LENGTH = 1050
    MAX_HEIGHT = 1050
    MAX_EDGES_SUM = 2000    # 2m
    MAX_WEIGHT = 30000      # 30kg

    PRODUCT_WIDTH = 340
    PRODUCT_DEPTH = 320
    PRODUCT_HEIGHT = 180
    PRODUCT_WEIGHT = 7700

    PRODUCT_QUANTITY = 17

    constraint1 = SimplePackageDimensionConstraint(MAX_WIDTH, MAX_LENGTH, MAX_HEIGHT, MAX_EDGES_SUM)
    constraint2 = WeightPackageConstraint(MAX_WEIGHT)

    packager = SimplePackager()
    assert packager._constraints == set()
    packager.add_constraint(constraint1)
    packager.add_constraint(constraint2)
    assert constraint1 in packager._constraints
    assert constraint2 in packager._constraints

    product = create_product(width=PRODUCT_WIDTH,
                             depth=PRODUCT_DEPTH,
                             height=PRODUCT_HEIGHT,
                             gross_weight=PRODUCT_WEIGHT,
                             sku='p1',
                             shop=get_default_shop(),
                             supplier=get_default_supplier())

    products = [product] * PRODUCT_QUANTITY
    packages = packager._pack_products(products)

    # adicionando 17 produtos iguais resultará em 6 caixas. 5 caixas ficarão com 3 itens cada
    # por causa da constraint de peso, 1 caixa terá 2 itens.
    # O tamanho das caixas com 3 itens é 34cm x 32cm x 54cm
    # O tamanho da caixa com 2 itens é 34cm x 32cm x 36cm

    assert len(packages) == 6

    # confere o tamanho e peso das primeiras 5 caixas
    for pkge_ix in range(5):
        assert packages[pkge_ix].width == 340
        assert packages[pkge_ix].length == 320
        assert packages[pkge_ix].height == 540
        assert packages[pkge_ix].weight == 23100
        assert packages[pkge_ix].count == 3
        assert packages[pkge_ix].volume == 340 * 320 * 540

    # confere o tamanho e peso da última caixa
    assert packages[5].width == 340
    assert packages[5].length == 320
    assert packages[5].height == 360
    assert packages[5].weight == 15400
    assert packages[5].count == 2
    assert packages[5].volume == 340 * 320 * 360


@pytest.mark.django_db
def test_simple_packager_impossible():
    """
    Products impossible to pack
    """
    MAX_WIDTH = 100
    MAX_LENGTH = 100
    MAX_HEIGHT = 100
    MAX_EDGES_SUM = 300
    MAX_WEIGHT = 30000

    PRODUCT_WIDTH = 200
    PRODUCT_DEPTH = 200
    PRODUCT_HEIGHT = 200
    PRODUCT_WEIGHT = 10000

    constraint1 = SimplePackageDimensionConstraint(MAX_WIDTH, MAX_LENGTH, MAX_HEIGHT, MAX_EDGES_SUM)
    constraint2 = WeightPackageConstraint(MAX_WEIGHT)

    packager = SimplePackager()
    assert packager._constraints == set()
    packager.add_constraint(constraint1)
    packager.add_constraint(constraint2)
    assert constraint1 in packager._constraints
    assert constraint2 in packager._constraints

    product = create_product(width=PRODUCT_WIDTH,
                             depth=PRODUCT_DEPTH,
                             height=PRODUCT_HEIGHT,
                             gross_weight=PRODUCT_WEIGHT,
                             sku='p1',
                             shop=get_default_shop(),
                             supplier=get_default_supplier())

    products = [product]
    packages = packager._pack_products(products)
    assert packages is None

    # produto inválido
    product.width = 0
    products = [product]
    packages = packager._pack_products(products)
    assert packages is None
