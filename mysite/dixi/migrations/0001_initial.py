# Generated by Django 3.2.8 on 2021-12-04 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_create', models.DateTimeField(auto_now=True)),
                ('owner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец корзины')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя категории')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товара',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_model', models.CharField(max_length=50, verbose_name='Материал')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Материал',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование модели')),
                ('slug', models.SlugField(unique=True)),
                ('amount', models.IntegerField(default=0, verbose_name='Количество товара')),
                ('season', models.IntegerField(choices=[(1, 'Демисезон'), (2, 'Лето'), (3, 'Зима')], verbose_name='Сезон')),
                ('factory', models.CharField(max_length=50, verbose_name='Фабрика')),
                ('size', models.IntegerField(default=36, verbose_name='Размер обуви')),
                ('gender', models.IntegerField(choices=[(1, 'Мужской'), (2, 'Женский')], verbose_name='Пол')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dixi.category', verbose_name='Категория')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dixi.material', verbose_name='Матераил')),
            ],
            options={
                'verbose_name': 'Модель',
                'verbose_name_plural': 'Модели',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('data', models.DateTimeField(auto_now=True)),
                ('owner', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('text', models.TextField(max_length=5000, verbose_name='Отзыв')),
                ('name_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='dixi.product', verbose_name='Название продукта')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='dixi.reviews', verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Цена товара')),
                ('discount_bool', models.BooleanField(default=False, verbose_name='Наличие скидки')),
                ('discount', models.PositiveIntegerField(blank=True, default=0, verbose_name='Скидка в %')),
                ('new_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, verbose_name='Цена товара с учетом скидки')),
                ('name_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price', to='dixi.product', verbose_name='Модель')),
            ],
            options={
                'verbose_name': 'Цена',
                'verbose_name_plural': 'Цены',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('phone_number', models.CharField(max_length=13, verbose_name='Номер телефона')),
                ('delivery_address', models.CharField(max_length=500, verbose_name='Адресс доставки')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('final_price', models.TextField(blank=True, verbose_name='Итоговая Цена')),
                ('order_date_create', models.DateTimeField(auto_now=True)),
                ('owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dixi.cart', verbose_name='Заказ Пользователя')),
            ],
            options={
                'verbose_name': 'Оформление заказа',
                'verbose_name_plural': 'Оформление заказа',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='Фото')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dixi.product', verbose_name='Наименование модели')),
            ],
            options={
                'verbose_name': 'Галерея',
                'verbose_name_plural': 'Галерея',
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=1, verbose_name='Количество товара')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, verbose_name='Общая Цена')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='dixi.cart', verbose_name='Корзина для пользователя')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dixi.product', verbose_name='Продукты в корзине')),
            ],
            options={
                'verbose_name': 'Товар в корзине',
                'verbose_name_plural': 'Товары в корзине',
            },
        ),
    ]