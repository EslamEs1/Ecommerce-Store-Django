
from products import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('list/', views.ProductList.as_view(), name='list'),
    path('list/filter/<int:min>/<int:max>/', views.ProductList.as_view(), name='filter_list_price'),
    path('list/<slug:slug>/', views.ProductList.as_view(), name='filter_list'),
    path('detail/<slug:slug>/', views.ProductDetail.as_view(), name='detail'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('toggle_wishlist/<slug:slug>/', views.toggle_wishlist, name='toggle_wishlist'),
    
]


