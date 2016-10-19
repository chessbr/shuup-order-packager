[![Build Status](https://travis-ci.org/rockho-team/shuup-order-packager.svg?branch=master)](https://travis-ci.org/rockho-team/shuup-order-packager)
[![Coverage Status](https://coveralls.io/repos/github/rockho-team/shuup-order-packager/badge.svg?branch=master)](https://coveralls.io/github/rockho-team/shuup-order-packager?branch=master)
[![License](https://img.shields.io/badge/license-AGPLv3-blue.svg)](LICENSE)

# Shuup Order Packager
Packing algorithms to put your basket/order products inside boxes.

## Usage
You can create packages from an order or even a basket:

```python
# add some constraints
constraint1 = SimplePackageDimensionConstraint(340, 230, 100, 1000)
constraint2 = WeightPackageConstraint(12000)

packager = SimplePackager()
packager.add_constraint(constraint1)
packager.add_constraint(constraint2)

packages = packager.pack_order(order)
# or
packages = packager.pack_basket(request.basket)

# do something with the packages
print(packages[0].width)
print(packages[0].height)
print(packages[0].length)
print(packages[0].weight)
print(packages[0].volume)
print(packages[0].count)
print(packages[0]._products)
```

`packages` is a list of `AbstractPackage` which you can check its width, length, height, weight and which products is inside.

## Customization
You can also create a custom Package and Constraint objects to fit you needs.

Our built-in SimplePackage just stack products inside, this way the final package size will be a kind of bounding-box of all products, taking into account constraints to limit the size/weight of the package.

## Compatibility
* Shuup v0.5.0
* [Tested on Python 3.4 and 3.5](https://travis-ci.org/rockho-team/shuup-order-packager)

Copyright
---------

Copyright (C) 2016 by [Rockho Team](https://github.com/rockho-team)

License
-------

Shuup Shipping Table is published under the GNU Affero General Public License,
version 3 (AGPLv3) (see the [LICENSE](LICENSE) file).
