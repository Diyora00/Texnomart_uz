from django.urls import path
from texnomart.views import (CategoryListView, CategoryDetailView, ProductListView, ProductDetailView,
                             AttributeKeyListView, AttributeValueListView)
from texnomart.token_auth import UserLoginAPIView
from texnomart.token_authjwt import LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category'),
    path('category/detail/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='category-detail'),
    path('product/detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('token-auth/', UserLoginAPIView.as_view(), name='token-auth'),
    path('api/token/', LoginAPIView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('attribute-key/', AttributeKeyListView.as_view(), name='attribute-key'),
    path('attribute-value/', AttributeValueListView.as_view(), name='attribute-value'),
]
