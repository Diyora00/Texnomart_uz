from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from texnomart.models import Category, Product
from django.core.mail import EmailMessage
from root.settings import BASE_DIR
import os
import json
from django.core.cache import cache


subject = 'Texnomart-uz'


@receiver(post_save, sender=Product)
@receiver(pre_delete, sender=Product)
def send_messages(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    if created:
        message = 'Product is created'
        to = 'jasurmavlonov24@gmail.com'
        email = EmailMessage(subject, message, to=[to])
        email.send()
        return
    file_name = os.path.join(BASE_DIR, 'texnomart/deleted_products', f'product_{instance.id}.json')
    data = {
        'id': instance.id,
        'title': instance.title,
        'description': instance.description,
        'price': instance.price,
        'category': instance.category.id,
        'discount': instance.discount,
    }
    with open(str(file_name), 'a') as file:
        json.dump(data, file, indent=4)


@receiver(post_save, sender=Category)
@receiver(pre_delete, sender=Category)
def send_messages(sender, instance, **kwargs):
    created = kwargs.get('created', False)
    if created:
        message = 'Category is created'
        to = 'jasurmavlonov24@gmail.com'
        email = EmailMessage(subject, message,  to=[to])
        email.send()
        return
    file_name = os.path.join(BASE_DIR, 'texnomart/deleted_categories', f'category_{instance.id}.json')
    data = {
        'id': instance.id,
        'title': instance.title,
        'slug': instance.slug,
        'image': str(instance.image),
    }
    with open(str(file_name), 'a') as file:
        json.dump(data, file, indent=4)


@receiver(pre_delete, sender=Category)
@receiver(pre_save, sender=Category)
def delete_cache_c(sender, instance, **kwargs):
    cache.delete(f'category_{instance.slug}')
    print('Detail cache deleted')
    cache.delete('category_list')
    print('List cache deleted')
