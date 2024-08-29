from django.db import models
from django.contrib.auth.models import User
from random import randint
from django.utils.text import slugify
from unidecode import unidecode


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, null=False, blank=True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    is_liked = models.ManyToManyField(User)
    discount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price*(1 - self.discount/100)
        return self.price


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)


class Comment(models.Model):
    class RatingChoice(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
    rating = models.PositiveIntegerField(choices=RatingChoice, default=RatingChoice.zero.value, null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')


class Key(models.Model):
    key_name = models.CharField(max_length=150)

    def __str__(self):
        return self.key_name


class Value(models.Model):
    value_name = models.CharField(max_length=150)

    def __str__(self):
        return self.value_name


class Attribute(models.Model):
    key = models.ForeignKey(Key, on_delete=models.CASCADE)
    value = models.ForeignKey(Value, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')

    def __str__(self):
        return self.product.title
