# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shuup_order_packager.constraints.simple import WeightPackageConstraint,\
    SimplePackageDimensionConstraint
from shuup.testing.factories import create_product
from shuup_order_packager.package.simple import SimplePackage
import pytest


@pytest.mark.django_db
def test_max_weight_constraint():
    constraint = WeightPackageConstraint(1500)
    package = SimplePackage()

    product1 = create_product(sku='p1', width=100, depth=200, height=50, gross_weight=2340)
    product2 = create_product(sku='p2', width=100, depth=200, height=50, gross_weight=690)

    # peso do product1 ultrapassa a constraint
    assert constraint.check(product1, package) is False

    # peso do product2 não ultrapassa a constraint
    assert constraint.check(product2, package) is True

    # adiciona o product2 no pacote
    package.add_product(product2)

    # ele ainda cabe no pacote
    assert constraint.check(product2, package) is True

    # adiciona de novo
    package.add_product(product2)

    # agora sem chances, o peso ultrapassa o máximo
    assert constraint.check(product2, package) is False


@pytest.mark.django_db
def test_dimensions_constraint():
    MAX_WIDTH = 450
    MAX_LENGTH = 200
    MAX_HEIGHT = 100
    MAX_EDGES_SUM = 740

    constraint = SimplePackageDimensionConstraint(MAX_WIDTH,
                                                  MAX_LENGTH,
                                                  MAX_HEIGHT,
                                                  MAX_EDGES_SUM)
    assert constraint.max_width == MAX_WIDTH
    assert constraint.max_length == MAX_LENGTH
    assert constraint.max_height == MAX_HEIGHT
    assert constraint.max_edges_sum == MAX_EDGES_SUM

    package = SimplePackage()

    # @test: produto com largura maior
    product = create_product(sku='p1', width=500, depth=200, height=100)
    assert constraint.check(product, package) is False

    # @test: produto com largura maior
    product = create_product(sku='p2', width=100, depth=300, height=460)
    assert constraint.check(product, package) is False

    # @test: produto com largura igual, comprimento maior
    product = create_product(sku='p3', width=450, depth=210, height=100)
    assert constraint.check(product, package) is False

    # @test: produto com largura igual, comprimento igual, altura maior
    product = create_product(sku='p4', width=450, depth=200, height=110)
    assert constraint.check(product, package) is False

    # @test: produto com largura ótimo
    product = create_product(sku='p5', width=440, depth=200, height=100)
    assert constraint.check(product, package) is True

    # @test: produto com largura menor
    product = create_product(sku='p6', width=300, depth=200, height=100)
    assert constraint.check(product, package) is True

    # @test: produto com largura menor
    product = create_product(sku='p7', width=100, depth=200, height=400)
    assert constraint.check(product, package) is True

    # @test: produto com tamanho maior
    product = create_product(sku='p8', width=500, depth=500, height=500)
    assert constraint.check(product, package) is False
    
    # @test: medidas excedem a soma das arestas
    product = create_product(sku='p11', width=450, depth=200, height=100)
    assert constraint.check(product, package) is False

    # adiciona um produto na caixa
    product9 = create_product(sku='p9', width=100, depth=200, height=50)
    assert constraint.check(product9, package) is True
    package.add_product(product9)

    # não serve por 10mm
    product10 = create_product(sku='p10', width=100, depth=200, height=60)
    assert constraint.check(product10, package) is False

    # o mesmo produto cabe 2x
    assert constraint.check(product9, package) is True

