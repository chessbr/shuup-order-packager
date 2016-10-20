# -*- coding: utf-8 -*-
# This file is part of Shuup Order Packager.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shuup_order_packager.algorithms._base import AbstractPackager
import pytest
from shuup_order_packager.constraints._base import AbstractPackageConstraint
from shuup_order_packager.package._base import AbstractPackage, BasePackage


def test_base_packager():
    base = AbstractPackager()

    with pytest.raises(NotImplementedError):
        base.new_package()
        
    with pytest.raises(NotImplementedError):
        base.add_constraint(None)
        
    with pytest.raises(NotImplementedError):
        base.product_fits(None, None)
        
    with pytest.raises(NotImplementedError):
        base.pack_source(None)
        
    with pytest.raises(NotImplementedError):
        base.pack_order(None)


def test_base_constraint():
    base = AbstractPackageConstraint()
    
    with pytest.raises(NotImplementedError):
        base.check(None, None)


def test_base_package():
    abspack = AbstractPackage()
    
    with pytest.raises(NotImplementedError):
        abspack.volume

    with pytest.raises(NotImplementedError):
        abspack.add_product(None)
        
    with pytest.raises(NotImplementedError):
        abspack.width
        
    with pytest.raises(NotImplementedError):
        abspack.height
        
    with pytest.raises(NotImplementedError):
        abspack.length

    with pytest.raises(NotImplementedError):
        abspack.weight
        
    with pytest.raises(NotImplementedError):
        abspack.count

    base_pkge = BasePackage()
    assert base_pkge.width == 0
    assert base_pkge.count == 0
    assert base_pkge.height == 0
    assert base_pkge.length == 0
    assert base_pkge.weight == 0
    assert base_pkge.volume == 0
    repr(base_pkge)
