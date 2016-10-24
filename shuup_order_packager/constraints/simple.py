# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.


from decimal import Decimal
import logging

from shuup_order_packager.utils import get_ordered_product_dimensions
from shuup_order_packager.constraints._base import AbstractPackageConstraint

logger = logging.getLogger(__name__)


class WeightPackageConstraint(AbstractPackageConstraint):
    """
    Package weight constraint: max weight in grams.
    """
    max_weight = Decimal()

    def __init__(self, max_weight):
        self.max_weight = Decimal(max_weight)

    def check(self, product, package):
        # não pode ultrapassar o peso máximo
        if package.weight + product.gross_weight > self.max_weight:
            return False

        return True


class SimplePackageDimensionConstraint(AbstractPackageConstraint):
    """
    Package dimensions constraint: max and min sizes in milimeters.
    This constraints will place products one on top of other, as a stack
    The final package size will be:
        (the larger product width, the larger product lenght, the sum of all heights)
    """
    max_width = Decimal()
    max_length = Decimal()
    max_height = Decimal()
    max_edges_sum = Decimal()

    def __init__(self, max_width, max_length, max_height, max_edges_sum):
        # ordena as dimensões da constraint
        constraint_sizes = [max_width, max_length, max_height]
        constraint_sizes.sort(reverse=True)
        max_width, max_length, max_height = constraint_sizes

        self.max_width = Decimal(max_width)
        self.max_length = Decimal(max_length)
        self.max_height = Decimal(max_height)
        self.max_edges_sum = Decimal(max_edges_sum)

    def check(self, product, package):
        width, length, height = get_ordered_product_dimensions(product)

        # não pode ultrapassar a largura máxima
        if max(package.width, width) > self.max_width:
            return False

        # não pode ultrapassar a profundidade máxima
        elif max(package.length, length) > self.max_length:
            return False

        # não pode ultrapassar a altura máxima
        elif package.height + height > self.max_height:
            return False

        # soma das arestas da caixa contendo o produto não pode ultrapassar a constraint
        elif self.max_edges_sum:
            package_edges_sum = (max(package.width, width) +
                                 max(package.length, length) +
                                 (package.height + height))

            if package_edges_sum > self.max_edges_sum:
                return False

        return True
