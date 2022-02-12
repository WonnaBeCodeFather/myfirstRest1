from .models import Price, Cart, CartProduct, OrderDetail, Category, Product, Material
from django.core.mail import send_mail
from django.db import transaction
from pytils.translit import slugify


class TotalPrice:
    def __init__(self, product, amount):
        self.get_product_price = Price.objects.get(product=product)
        self.amount = amount

    def get_total_price(self):
        if self.get_product_price.new_price:
            return self.get_product_price.new_price * self.amount
        return self.get_product_price.price * self.amount


class Discount:
    def __init__(self, price, discount):
        self.price = price
        self.discount = discount

    def discount_price(self):
        if self.discount:
            new_price = float(self.price) - ((float(self.price) / 100) * float(self.discount))
            return new_price
        else:
            new_price = 0
            return new_price


class GetOrCreateCart:
    def __init__(self, user):
        self.user = user

    def get_or_create_cart(self):
        return Cart.objects.get_or_create(owner=self.user)[0]


class CheckDuplicateProduct(GetOrCreateCart):
    def __init__(self, user, product):
        super().__init__(user)
        self.product = product

    def check_duplicate_product_in_cart(self):
        get_cartproduct_list = CartProduct.objects.filter(product=self.product, owner=self.get_or_create_cart())
        if not get_cartproduct_list:
            return True
        return False


class DuplicateFinded(CheckDuplicateProduct):
    def __init__(self, user, product, amount):
        super(DuplicateFinded, self).__init__(user, product)
        self.amount = amount

    def duplicate_finded(self):
        get_product_in_cartproduct = CartProduct.objects.get(product=self.product, owner=self.get_or_create_cart())
        get_product_in_cartproduct.amount = get_product_in_cartproduct.amount + self.amount
        get_product_in_cartproduct.price = get_product_in_cartproduct.price + TotalPrice(self.product,
                                                                                         self.amount).get_total_price()
        get_product_in_cartproduct.save()
        return get_product_in_cartproduct


# class CartProductService:
#     def __init__(self, user):
#         self.user = user
#         self.cart_queryset_user = Cart.objects.get_or_create(owner=self.user)[0]
#
#     def check_duplicate_product_in_cart(self, product):
#         get_cartproduct_list = CartProduct.objects.filter(product=product, owner=self.cart_queryset_user)
#         if not get_cartproduct_list:
#             return True
#         return False
#
#     def duplicate_finded(self, product, amount):
#         get_product_in_cartproduct = CartProduct.objects.get(product=product, owner=self.cart_queryset_user)
#         get_product_in_cartproduct.amount = get_product_in_cartproduct.amount + amount
#         get_product_in_cartproduct.price = get_product_in_cartproduct.price + TotalPrice(product).get_total_price(
#             amount)
#         get_product_in_cartproduct.save()
#         return get_product_in_cartproduct
#
#     def clean_cartproduct(self):
#         return CartProduct.objects.filter(owner=self.cart_queryset_user).delete()

class CartProductList(GetOrCreateCart):
    def __init__(self, user):
        super().__init__(user)
        self.cartproduct_list = CartProduct.objects.filter(owner=self.get_or_create_cart())


class CleanCart(CartProductList):
    def clean_cart(self):
        return self.cartproduct_list.delete()


class OrderTotalPrice(CartProductList):
    def get_total_price_all_cartproduct(self):
        total_price = []
        for i in self.cartproduct_list:
            total_price.append(i.price)
        return sum(total_price)


class CreateOrderDetail(CartProductList):
    def __init__(self, user, order):
        super(CreateOrderDetail, self).__init__(user)
        self.order = order

    def create_order_detail(self):
        for i in self.cartproduct_list:
            OrderDetail.objects.create(product=i.product, order=self.order, amount=i.amount, size=i.size)


class SendMailSalesman:
    def __init__(self, order):
        self.order = order

    def send_mail_after_order(self):
        send_mail(subject='Новый заказ!',
                  message=f"Имя - {self.order.first_name},\n "
                          f"Фамилия - {self.order.last_name},\n"
                          f"Номер телефона - {self.order.phone_number},\n"
                          f"Адресс Доставки - {self.order.delivery_address},\n"
                          f"Комментарии - {self.order.description},\n"
                          f"Сумма заказа - {self.order.final_price},\n"
                          f"Продукт и размер {[i.size for i in OrderDetail.objects.filter(order=self.order)]}",
                  from_email='djangodixi@gmail.com',
                  recipient_list=['opiumdlyanaroda3319@gmail.com'])


# class OrderService:
#     def __init__(self, owner):
#         self.owner = owner
#         self.cartproduct_list = CartProduct.objects.filter(owner=Cart.objects.get(owner=owner))
#
#     def get_total_price_all_cartproduct(self):
#         total_price = []
#         for i in self.cartproduct_list:
#             total_price.append(i.price)
#         return sum(total_price)
#
#     def set_order_for_order_product(self, order):
#         for i in self.cartproduct_list:
#             OrderDetail.objects.create(product=i.product, order=order, amount=i.amount, size=i.size)
#
#     @staticmethod
#     def send_mail_after_order(order):
#         send_mail(subject='Новый заказ!',
#                   message=f"Имя - {order.first_name},\n "
#                           f"Фамилия - {order.last_name},\n"
#                           f"Номер телефона - {order.phone_number},\n"
#                           f"Адресс Доставки - {order.delivery_address},\n"
#                           f"Комментарии - {order.description},\n"
#                           f"Сумма заказа - {order.final_price},\n"
#                           f"Продукт и размер {[i.size for i in OrderDetail.objects.filter(order=order)]}",
#                   from_email='djangodixi@gmail.com',
#                   recipient_list=['opiumdlyanaroda3319@gmail.com'])


class CreateProductService:
    def __init__(self, data):
        self.data = data

    def __create_product(self):
        get_material = Material.objects.get(id=self.data['material'])
        get_category = Category.objects.get(id=self.data['category'])
        get_slug = slugify(self.data['title'])
        return Product.objects.create(title=self.data['title'],
                                      slug=get_slug,
                                      season=self.data['season'],
                                      factory=self.data['factory'],
                                      gender=self.data['gender'],
                                      category=get_category,
                                      material=get_material)

    def __create_price(self, product):
        set_new_price = Discount(self.data['price']['price'], self.data['price']['discount']).discount_price()
        return Price.objects.create(product=product,
                                     price=self.data['price']['price'],
                                     discount=self.data['price']['discount'],
                                     new_price=set_new_price)

    @transaction.atomic
    def fill_product(self):
        product = self.__create_product()
        price = self.__create_price(product)
