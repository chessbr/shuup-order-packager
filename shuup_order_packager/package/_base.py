# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from decimal import Decimal


class AbstractPackage(object):
    """
    An abstract package class.
    """

    @property
    def volume(self):
        """
        Calculates the volume of the package
        :rtype: decimal.Decimal
        """
        raise NotImplementedError("Implement this method")

    def add_product(self, product):
        """
        Adds a product to the package
        :type product: shuup.core.models.Product
        """
        raise NotImplementedError("Implement this method")

    @property
    def width(self):
        """ Return the width of the package """
        raise NotImplementedError("Implement this method")

    @property
    def height(self):
        """
        Return the height of the package
        :rtype: decimal.Decimal
        """
        raise NotImplementedError("Implement this method")

    @property
    def length(self):
        """
        Return the length of the package
        :rtype: decimal.Decimal
        """
        raise NotImplementedError("Implement this method")

    @property
    def weight(self):
        """
        Return the weight of the package
        :rtype: decimal.Decimal
        """
        raise NotImplementedError("Implement this method")

    @property
    def count(self):
        """
        Return the quantity of items inside this package
        :rtype: int
        """
        raise NotImplementedError("Implement this method")


class BasePackage(AbstractPackage):
    """
    Base package class. This objects does not controls or update
    the package size when product are added.
    You must subclass this class and implement your custom logic, if you need.
    """
    _width = Decimal(0.0)
    _height = Decimal(0.0)
    _length = Decimal(0.0)
    _weight = Decimal(0.0)
    _products = []

    def __init__(self):
        self._width = Decimal(0.0)
        self._height = Decimal(0.0)
        self._length = Decimal(0.0)
        self._weight = Decimal(0.0)
        self._products = []

    @property
    def volume(self):
        return (self.width * self.height * self.length)

    def add_product(self, product):
        self._products.append(product)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def length(self):
        return self._length

    @property
    def weight(self):
        return self._weight

    @property
    def count(self):
        return len(self._products)

    def __repr__(self, *args, **kwargs):
        return "<Package: items:{0}, width={1}mm, "\
               "height: {2}mm, length={3}mm, "\
               "weight={4}g>".format(self.count,
                                     self.width,
                                     self.height,
                                     self.length,
                                     self.weight)
