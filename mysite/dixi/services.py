from .models import Price, Cart, CartProduct, OrderDetail, Category, Product, Material
from django.core.mail import send_mail
from django.db import transaction


class PriceService:
    def __init__(self, product=None):
        if product:
            self.product = product
            self.get_product_price = Price.objects.get(product=product)

    # @staticmethod
    # def discount_price(price, discount):
    #     if discount:
    #         new_price = float(price) - ((float(price) / 100) * float(discount))
    #         new_price = new_price
    #         return new_price
    #     else:
    #         new_price = 0
    #         return new_price

    def get_total_price(self, amount):
        if self.get_product_price.new_price:
            return self.get_product_price.new_price * amount
        return self.get_product_price.price * amount


class CartProductService:
    def __init__(self, user):
        self.user = user
        self.cart_queryset_user = Cart.objects.get_or_create(owner=self.user)[0]

    def check_duplicate_product_in_cart(self, product):
        get_cartproduct_list = CartProduct.objects.filter(product=product, owner=self.cart_queryset_user)
        if not get_cartproduct_list:
            return True
        return False

    def duplicate_finded(self, product, amount):
        get_product_in_cartproduct = CartProduct.objects.get(product=product, owner=self.cart_queryset_user)
        get_product_in_cartproduct.amount = get_product_in_cartproduct.amount + amount
        get_product_in_cartproduct.price = get_product_in_cartproduct.price + PriceService(product).get_total_price(
            amount)
        get_product_in_cartproduct.save()
        return get_product_in_cartproduct

    def clean_cartproduct(self):
        return CartProduct.objects.filter(owner=self.cart_queryset_user).delete()


class OrderService:
    def __init__(self, owner):
        self.owner = owner
        self.cartproduct_list = CartProduct.objects.filter(owner=Cart.objects.get(owner=owner))

    def get_total_price_all_cartproduct(self):
        total_price = []
        for i in self.cartproduct_list:
            total_price.append(i.price)
        return sum(total_price)

    def set_order_for_order_product(self, order):
        for i in self.cartproduct_list:
            OrderDetail.objects.create(product=i.product, order=order, amount=i.amount, size=i.size)

    @staticmethod
    def send_mail_after_order(order):
        send_mail(subject='Новый заказ!',
                  message=f"Имя - {order.first_name},\n "
                          f"Фамилия - {order.last_name},\n"
                          f"Номер телефона - {order.phone_number},\n"
                          f"Адресс Доставки - {order.delivery_address},\n"
                          f"Комментарии - {order.description},\n"
                          f"Сумма заказа - {order.final_price},\n"
                          f"Продукт и размер {[i.size for i in OrderDetail.objects.filter(order=order)]}",
                  from_email='djangodixi@gmail.com',
                  recipient_list=['opiumdlyanaroda3319@gmail.com'])


class SuperService:

    def __init__(self, data):
        self.data = data

    @transaction.atomic
    def main(self):
        SuperService(self.data).create_product()

    def create_product(self):
        get_material = Material.objects.get(id=self.data['material'])
        get_category = Category.objects.get(id=self.data['category'])
        product = Product.objects.create(title=self.data['title'],
                                         season=self.data['season'],
                                         factory=self.data['factory'],
                                         gender=self.data['gender'],
                                         category=get_category,
                                         material=get_material)
        return SuperService(self.data).create_price(product)

    def create_price(self, product):
        set_new_price = 0.00
        if self.data['price']['discount']:
            new_price = float(self.data['price']['price']) - ((float(self.data['price']['price']) / 100)
                                                              * float(self.data['price']['discount']))
            set_new_price = new_price

        price = Price.objects.create(product=product,
                                     price=self.data['price']['price'],
                                     discount=self.data['price']['discount'],
                                     new_price=set_new_price)
        return price
