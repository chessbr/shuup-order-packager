# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from ._base import BasePackage

import logging
from shuup_order_packager.utils import get_ordered_product_dimensions
logger = logging.getLogger(__name__)


class SimplePackage(BasePackage):
    """
    Implementação do pacote simples
    O pacote sempre terá as dimensões ordenadas em: largura, comprimento e altura
    Todo e qualquer item será colocado na caixa nessa ordem:
        * itens mais largos
        * itens mais compridos
        * items mais altos
    O tamanho do pacote terá a largura e comprimento do maior
    produto que está dentro da caixa.
    A altura será a soma da altura de todos os itens.
    """

    def add_product(self, product):
        width, length, height = get_ordered_product_dimensions(product)

        # soma o peso e a altura
        self._weight = self._weight + product.gross_weight
        self._height = self._height + height

        # faz a bounding box atribuindo sempre a largura e comprimento do pacote
        # com as dimensões do maior item
        self._width = max(self._width, width)
        self._length = max(self._length, length)

        super(SimplePackage, self).add_product(product)

    @property
    def volume(self):
        return self.width * self.length * self.height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def length(self):
        return self._length
