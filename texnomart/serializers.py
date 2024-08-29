from django.db.models import Avg, Count
from django.db.models.functions import Round
from texnomart.models import Category, Product, Key, Value
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_primary_image(self, obj):
        image = obj.images.filter(is_primary=True).first()
        request = self.context['request']
        if image:
            return request.build_absolute_uri(image.image.url)
        return None

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user in obj.is_liked.all() and user.is_authenticated:
            return True
        return False

    def get_all_images(self, obj):
        return self.context.get('all_images', [])

    def get_attributes(self, instance):
        return self.context.get('attributes', [])

    def get_comments(self, obj):
        return self.context.get('comments', [])

    def get_rating(self, obj):
        return obj.comments.aggregate(avg=Round(Avg('rating')))['avg']

    def get_comment_count(self, obj):
        return self.context.get('comment_count', 'go to detail')


class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = '__all__'