from decimal import Decimal
from django.conf import settings
from products.models import Product


class Basket:
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        voucher = self.session.get(settings.VOUCHER_SESSION_ID)
        if settings.VOUCHER_SESSION_ID not in request.session:
            voucher = self.session[settings.VOUCHER_SESSION_ID] = {"discount": 0, "code": None}
        self.basket = basket
        self.voucher = voucher

    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        else:
            # if self.voucher["discount"] > 0:
                # self.basket[product_id] = {"price": int(product.final_price - (product.final_price * self.voucher["discount"] / 100)), "qty": qty}
            # else:
            self.basket[product_id] = {"price": str(product.final_price), "qty": qty}

        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item["qty"] for item in self.basket.values())

    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        self.save()

    def get_total_price_without_discount(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
    
    def get_total_price(self):
        price = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        if self.voucher["discount"] != 0:
            price = price - (price * self.voucher["discount"] / 100)
        return round(price, 2)

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            if self.basket.__len__() == 0:
                del self.session[settings.VOUCHER_SESSION_ID]
            self.save()

    def set_discount(self, code, discount):
        self.voucher["discount"] = discount
        self.voucher["code"] = code
        self.save()
    
    def save(self):
        self.session.modified = True

    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        del self.session[settings.VOUCHER_SESSION_ID]
        self.save()


""" 
Code in this file has been inspried/reworked from other known works. Plese ensure that
the License below is included in any of your work that is directly copied from
this source file.


MIT License

Copyright (c) 2019 Packt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 
"""
