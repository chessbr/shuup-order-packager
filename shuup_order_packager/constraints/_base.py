# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.


class AbstractPackageConstraint(object):
    """
    Abstract class with package constraints
    """

    def check(self, product, package):
        """
        Validate if the product can be put inside the package

        :param: product shuup.core.models.Product
        :param: package shuup_order_packager.package.AbstractPackage

        :rtype: bool
        :return: whether the product can be put inside the package
        """
        raise NotImplementedError("Implement this method")
