# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.


class AbstractPackager(object):
    """
    Abstract class to pack products in packages
    """
    package_class = None

    def new_package(self):
        """
        Creates and returns a brand-new package
        :rtype shuup_order_packager.package.AbstractPackage
        """
        raise NotImplementedError("Implement this method")

    def add_constraint(self, package_constraint):
        """
        Adds the a packager constraint. Packages will be validated against all added contraints.
        :type package_constraint: shuup_order_packager.constraints.AbstractPackageConstraint
        """
        raise NotImplementedError("Implement this method")

    def product_fits(self, product, package):
        """
        Indicates whether the product fits in the package
        :type product: shuup.core.models.Product
        :type package: shuup_order_packager.package.AbstractPackage
        :param: product: the product to check whether it fits or not
        :param: package: the package to check
        :rtype: bool
        :return: whether the product fits in the package
        """
        raise NotImplementedError("Implement this method")

    def pack_source(self, source):
        """
        Pack products of a OrderSource
        :type source: shuup.core.order_creator.OrderSource
        :rtype: Iterable[Package]
        """
        raise NotImplementedError("Implement this method")

    def pack_order(self, order):
        """
        Pack products of a Order
        :type source: shuup.core.models.Order
        :rtype: Iterable[Package]
        """
        raise NotImplementedError("Implement this method")
