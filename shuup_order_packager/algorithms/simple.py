# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import logging

from shuup_order_packager.package.simple import SimplePackage
from shuup_order_packager.algorithms._base import AbstractPackager
logger = logging.getLogger(__name__)


class SimplePackager(AbstractPackager):
    package_class = SimplePackage

    def __init__(self):
        self._constraints = set()

    def new_package(self):
        """
        Creates and returns a brand-new package which we know how to deal with.
        """
        return self.package_class()

    def add_constraint(self, constraint):
        self._constraints.add(constraint)

    def product_fits(self, product, package):
        if not self._product_has_valid_attrs(product):
            return False

        for constraint in self._constraints:
            if not constraint.check(product, package):
                return False

        return True

    def _product_has_valid_attrs(self, product):
        """
        Valida se o produto possui atributos válidos.
        :rtype: bool
        :return: se o produto está apto a ser adicionado em alguma caixa
        """

        # valida se o produto está bem configurado
        if not product.width or not product.depth or not product.height or not product.gross_weight:
            logger.warn("SimplePackage: Produto {0} (id={1}) mal configurado. "
                        "Configure corretamente as dimensoes e peso do produto.".format(product, product.id))
            return False
        return True

    def pack_source(self, source):
        # expande os itens do pedido, para que cada produto
        # seja colocado separadamente na caixa
        products = []

        for line in source.get_product_lines():
            products.extend([line.product] * line.quantity)

        return self._pack_products(products)

    def pack_order(self, order):
        # expande os itens do pedido, para que cada produto
        # seja colocado separadamente na caixa
        products = []
        product_lines = [l for l in order.lines.products()]

        for line in product_lines:
            products.extend([line.product] * int(line.quantity))

        return self._pack_products(products)

    def _pack_products(self, products):
        """
        Calcula os atributos dos produtos e cria pacotes
        contendo o peso e tamanho das embalagens finais.
        Se o tamanho ou peso ultrapassar os limites
        estabelecidos pelos, uma nova encomenda será criada.
        Atualmente o algoritmo vai somando a altura dos produtos
        até chegar a uma altura limite. Quando chegar na altura limite
        o pacote é fechado e outro é criado.
        :param: products: lista de produtos a serem empacotados
        :type: products Itetable[shuup.core.models.Product]
        :rtype: Iterable[shuup_order_packager.package.AbstractPackage|None]
        :return: Lista de pacotes ou None se for impossível
        """

        packages = []

        # GAMBI: coloca num dicionário para poder acessar
        # no escopo da função interna close_package
        current_package = {'default': self.new_package()}

        def close_package():
            """ Se o pacote possui itens, fecha e cria um novo """
            if current_package['default'].count > 0:
                packages.append(current_package['default'])
            current_package['default'] = self.new_package()

        for product in products:
            # opa, produto não serviu! vamos testar com um pacote vazio
            if not self.product_fits(product, current_package['default']):

                # cria um pacote temporario e testa se ele serve em um vazio
                if self.product_fits(product, self.new_package()):
                    # ok, se é possível então fecha esse e cria um novo
                    close_package()

                else:
                    # Impossível acondicionar o produto em um pacote vazio
                    # não podemos efetuar a entrega como um todo
                    return None

            current_package['default'].add_product(product)

        close_package()
        return packages
