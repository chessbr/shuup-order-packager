# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.


def get_ordered_product_dimensions(product):
    """
    Returns a reversed ordered (greater first) tuple with 
    product's width, height and depth
    :type: product: shuup.core.models.Product
    """

    height = product.height
    width = product.width
    length = product.depth

    # obtém as dimensões e ordena
    # assim teremos a largura como a maior dimensão
    # precedida do comprimento..
    # a altura será a menor dimensão
    sizes = [width, length, height]
    sizes.sort(reverse=True)
    width, length, height = sizes

    return width, length, height
