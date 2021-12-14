import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from pytils.translit import slugify


class Product(models.Model):
    class Gender(models.IntegerChoices):
        Men = 1, 'Мужской'
        Women = 2, 'Женский'

    class Season(models.IntegerChoices):
        demi = 1, 'Демисезон'
        summer = 2, 'Лето'
        winter = 3, 'Зима'

    name = models.CharField(max_length=100, verbose_name='Наименование модели')
    material = models.ForeignKey('Material', on_delete=models.CASCADE, verbose_name='Матераил')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(unique=True, blank=True, null=True, help_text='<font color="red">'
                                                                          'Поле заполняется автоматически!</font>')
    amount = models.IntegerField(verbose_name='Количество товара', default=0)
    season = models.IntegerField(verbose_name='Сезон', choices=Season.choices)
    factory = models.CharField(max_length=50, verbose_name='Фабрика')
    size = models.IntegerField(verbose_name='Размер обуви', default=36)
    gender = models.IntegerField(verbose_name='Пол', choices=Gender.choices)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def save(self, *args, **kwargs):
        get_name = str(self.name) + str(self.size)
        self.slug = slugify(get_name)
        super(Product, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товара'


class Price(models.Model):
    name_model = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Модель',
                                   related_name='price')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена товара', default=00.00,
                                )
    discount_bool = models.BooleanField(default=False, verbose_name='Наличие скидки')
    discount = models.PositiveIntegerField(default=0, blank=True, verbose_name='Скидка в %')
    new_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена товара с учетом скидки',
                                    default=00.00, blank=True, help_text='<font color="red">'
                                                                         'Цена пересчитывается автоматически,'
                                                                         'поле заполнять не нужно!</font>')

    def __str__(self):
        return f'Цена для {self.name_model}'

    """Если поле discount_bool = True, то автоматически заполнятеся поле new_price с учётом указанной скидки в 
    процентах, а иначе поля new_price и discount устанавливаются в 0. Поле price остаётся неизменным в любом случае.
    """

    def save(self, *args, **kwargs):
        if self.discount_bool:
            new_price = float(self.price) - (float(self.price) * (float(self.discount) / 100))
            self.new_price = new_price
        else:
            self.new_price = 0.00
            self.discount = 0
        super(Price, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


@receiver(post_save, sender=Price)
def testsignal(sender, instance, created, **kwargs):
    print(instance.name_model)
    print('Закомитьменяполностью')


class Material(models.Model):
    name_model = models.CharField(max_length=50, verbose_name='Материал')

    def __str__(self):
        return self.name_model

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материал'


class Gallery(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Наименование модели')
    image = models.ImageField(verbose_name='Фото', null=True)

    def __str__(self):
        return f'Фотография {self.name}'

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'


class Reviews(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=100, verbose_name='Имя')
    text = models.TextField(max_length=5000, verbose_name='Отзыв')
    name_product = models.ForeignKey(Product, verbose_name='Название продукта', on_delete=models.CASCADE,
                                     related_name='reviews')
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.CASCADE, blank=True, null=True,
                               related_name='children')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв на модель {self.name_product}'


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Владелец корзины', null=True, blank=True)
    data_create = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для пользователя {self.owner}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    """При создании новой корзины проверяется есть ли корзины созданные 14 дней назад и если они есть, то эти корзины
     удаляются. Это связанно с тем, что корзину для анонимного пользователя я привязал к сессии срок котрой ровно 14 
     дней"""

    def save(self, *args, **kwargs):
        now = datetime.datetime.now() - datetime.timedelta(days=14)
        super().save(*args, **kwargs)
        Cart.objects.filter(data_create__lte=now).delete()


class CartProduct(models.Model):
    owner = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина для пользователя', null=True,
                              blank=True, related_name='product')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукты в корзине')
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество товара')
    price = models.DecimalField(decimal_places=2, max_digits=7, blank=True, verbose_name='Общая Цена')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'Товары пользователя {self.owner}'

    """Если на продукт в корзине есть скидка то в общую стоимость продукта входит цена с учётом скидки. Так же если
    в корзине содержатся модели обуви с одинаковым названием но с разными размерами то цена подтягивается по названию
    обуви. Если пользователь добавляет товар в корзину повторно, то он не добавляются"""

    def save(self, *args, **kwargs):
        get_name = self.products.name
        get_first_id = Product.objects.filter(name=get_name)[0].pk
        if Price.objects.get(name_model=get_first_id).discount_bool:
            self.price = Price.objects.get(name_model=self.products).new_price
            self.price = self.price * self.amount
        else:
            self.price = Price.objects.get(name_model=get_first_id).price
            self.price = self.price * self.amount
        if not CartProduct.objects.filter(owner=self.owner):
            super(CartProduct, self).save(*args, **kwargs)
        else:
            for i in CartProduct.objects.filter(owner=self.owner):
                if i.products != self.products:
                    super(CartProduct, self).save(*args, **kwargs)


class Order(models.Model):
    owner = models.OneToOneField(Cart, on_delete=models.SET_NULL, verbose_name='Заказ Пользователя', null=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона')
    delivery_address = models.CharField(max_length=500, verbose_name='Адресс доставки')
    description = models.TextField(verbose_name='Комментарий', blank=True, null=True)
    final_price = models.TextField(verbose_name='Итоговая Цена', blank=True)
    order_date_create = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Оформление заказа'
        verbose_name_plural = verbose_name

    """Пересчет общей суммы заказа всех товаров в корзине. Отправка письма продавцу на почту со всем содержимым заказа.
    После оформления заказа, количество проданного товара вычитается из общего количества товара в модели Product
    """

    def save(self, *args, **kwargs):
        lists = []
        for i in CartProduct.objects.filter(owner=self.owner):
            lists.append(float(i.price))
        self.final_price = sum(lists)
        send_mail(subject='Test', message=f'Имя - {self.first_name},\n '
                                          f'Фамилия - {self.last_name},\n'
                                          f'Номер телефона - {self.phone_number},\n'
                                          f'Адресс Доставки - {self.delivery_address},\n'
                                          f'Комментарии - {self.description},\n'
                                          f'Сумма заказа - {self.final_price},\n'
                                          f'Продукт и размер {({str(i.products): str(i.products.size) for i in CartProduct.objects.filter(owner=self.owner.pk)})},',
                  from_email='djangodixi@gmail.com',
                  recipient_list=['opiumdlyanaroda3319@gmail.com'])
        for i in CartProduct.objects.filter(owner=self.owner):
            get_cartproduct = CartProduct.objects.get(id=i.pk).products.pk
            get_cartproduct_amount = CartProduct.objects.get(id=i.pk).amount
            get_product = Product.objects.get(id=get_cartproduct)
            get_product.amount = get_product.amount - get_cartproduct_amount
            get_product.save()
        super().save(*args, **kwargs)
        CartProduct.objects.filter(owner=self.owner.pk).delete()

    def __str__(self):
        return f'Заказ для {self.last_name} {self.first_name}'
