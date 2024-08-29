from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from texnomart.models import Category, Product, Key, Value
from texnomart.serializers import CategorySerializer, ProductSerializer, AttributeKeySerializer, AttributeValueSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from texnomart.permissions import CustomPermissionForProduct
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


class CategoryListView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        post_key = 'category_list'
        categories = cache.get(post_key)
        if not categories:
            categories = Category.objects.all()
            result = self.paginate_queryset(categories, request, view=self)
            serializer = CategorySerializer(result, many=True)
            cache.set(post_key, serializer.data, timeout=60 * 5)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(categories)


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        category_key = f'category_{self.kwargs['slug']}'
        category = cache.get(category_key)
        if not category:
            category = Category.objects.get(slug=kwargs['slug'])
            serializer = CategorySerializer(category)
            cache.set(category_key, serializer.data, timeout=60*5)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(category)

    def put(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, slug):
        category = Category.objects.get(slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(generics.ListCreateAPIView):
    permission_classes = [CustomPermissionForProduct]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['price', 'discount']
    search_fields = ['title']

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Product.objects.filter(category__slug=slug).select_related('category').prefetch_related('is_liked')


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CustomPermissionForProduct]
    queryset = Product.objects.all().annotate(comment_count=Count('comments'))
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        obj = self.queryset.get(pk=self.kwargs['pk'])
        if obj:
            context['all_images'] = [self.request.build_absolute_uri(image.image.url) for image in obj.images.all()]

            attributes = {i.key.key_name: i.value.value_name for i in obj.attributes.all()}
            context['attributes'] = attributes

            context['comments'] = obj.comments.all().values('message', 'rating', 'user__username')
            context['comment_count'] = obj.comment_count
        return context


class AttributeKeyListView(generics.ListCreateAPIView):
    queryset = Key.objects.all()
    serializer_class = AttributeKeySerializer


class AttributeValueListView(generics.ListCreateAPIView):
    queryset = Value.objects.all()
    serializer_class = AttributeValueSerializer


class AllProductListView(generics.ListAPIView):
    queryset = Product.objects.all().select_related('category').prefetch_related('is_liked')
    serializer_class = ProductSerializer
