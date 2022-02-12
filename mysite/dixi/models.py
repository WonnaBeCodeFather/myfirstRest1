from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Product(models.Model):
    class Gender(models.IntegerChoices):
        Men = 1, 'Мужской'
        Women = 2, 'Женский'

    class Season(models.IntegerChoices):
        demi = 1, 'Демисезон'
        summer = 2, 'Лето'
        winter = 3, 'Зима'

    title = models.CharField(max_length=100, verbose_name='Наименование модели')
    material = models.ForeignKey('Material', on_delete=models.CASCADE, verbose_name='Матераил', related_name='material')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(unique=True, blank=True, null=True, help_text='<font color="red">'
                                                                          'Поле заполняется автоматически!</font>')
    season = models.IntegerField(verbose_name='Сезон', choices=Season.choices)
    factory = models.CharField(max_length=50, verbose_name='Фабрика')
    gender = models.IntegerField(verbose_name='Пол', choices=Gender.choices)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


class Size(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name='Наименование модели', null=True,
                                related_name='size')
    size = models.PositiveIntegerField(default=36)
    amount = models.IntegerField(verbose_name='Количество товара', default=0)

    def __str__(self):
        return f'{self.product} : {self.size}'

    class Meta:
        verbose_name = 'Размер обуви'
        verbose_name_plural = "Размеры обуви"


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товара'


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Модель',
                                related_name='price')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена товара', default=00.00,
                                )
    discount = models.PositiveIntegerField(default=0, blank=True, verbose_name='Скидка в %', null=True)
    new_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена товара с учетом скидки',
                                    default=00.00, blank=True, help_text='<font color="red">'
                                                                         'Цена пересчитывается автоматически,'
                                                                         'поле заполнять не нужно!</font>')

    def __str__(self):
        return f'Цена для {self.product}'

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


class Material(models.Model):
    name = models.CharField(max_length=50, verbose_name='Материал')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материал'


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Наименование модели',
                                related_name='image')
    image = models.ImageField(verbose_name='Фото', null=True)

    def __str__(self):
        return f'Фотография {self.product}'

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'


class Reviews(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=100, verbose_name='Имя')
    text = models.TextField(max_length=5000, verbose_name='Отзыв')
    product = models.ForeignKey(Product, verbose_name='Название продукта', on_delete=models.CASCADE,
                                related_name='reviews')
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.CASCADE, blank=True, null=True,
                               related_name='children')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв на модель {self.product}'


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Владелец корзины', null=True, blank=True)
    data_create = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для пользователя {self.owner}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'


class CartProduct(models.Model):
    owner = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина для пользователя', null=True,
                              blank=True, related_name='product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукты в корзине')
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество товара')
    price = models.DecimalField(decimal_places=2, max_digits=7, blank=True, verbose_name='Общая Цена')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Размер продукта', related_name='sizes')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'Товары пользователя {self.owner}'


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="наименование товара")
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, verbose_name="Номер заказа")
    amount = models.PositiveIntegerField(verbose_name="Количество товара в заказе")
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, verbose_name='Размер продукта', null=True)

    class Meta:
        verbose_name = 'Товары в заказе'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Order: {self.order.pk} | Product: {self.product} | Size: {self.size}'


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

    def __str__(self):
        return f'Заказ для {self.last_name} {self.first_name}'
