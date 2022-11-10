from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ProductsView.as_view(), name='products'),
    # path('<str:category>/', views.ProductsView.as_view(), name='products'),
    path('<str:id>/', views.ProductDetailView.as_view(), name='products-item'),


    # path('', views.ProductsView.as_view(), name='productsss'),
    # path('<str:category>/', views.ProductsView.as_view(), name='products'),
    # path('<str:category>/<str:id>/', views.ProductDetailView.as_view(), name='products-item'),
    
]
