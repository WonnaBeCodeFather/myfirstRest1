from django.db import models
from django.urls import reverse


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
    slug = models.SlugField(unique=True)
    amount = models.IntegerField(verbose_name='Количество товара', default=0)
    season = models.CharField(max_length=50, verbose_name='Сезон', choices=Season.choices)
    factory = models.CharField(max_length=50, verbose_name='Фабрика')
    size = models.IntegerField(verbose_name='Размер обуви', default=36)
    gender = models.CharField(max_length=50, verbose_name='Пол', choices=Gender.choices)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товара'


class Price(models.Model):
    name_model = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='Модель',
                                      related_name='price_model_1')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена товара', default=00.00)
    discount_bool = models.BooleanField(default=False, verbose_name='Наличие скидки')
    discount = models.PositiveIntegerField(default=0, blank=True, verbose_name='Скидка в %')
    new_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена товара с учетом скидки',
                                    default=00.00, blank=True)

    def __str__(self):
        return f'Цена для {self.name_model}'

    def save(self, *args, **kwargs):
        if self.discount_bool:
            new_price = float(self.price) - (float(self.price) * (float(self.discount) / 100))
            self.new_price = new_price
        else:
            self.new_price = 0.00
        super(Price, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


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
    email = models.EmailField()
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
