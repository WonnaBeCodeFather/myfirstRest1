from django.urls import path

from . import views

urlpatterns = [
    path('product/', views.ProductListView.as_view()),
    path('product/<int:pk>/', views.ProductDetailView.as_view()),

    path('reviews/', views.ReviewsView.as_view()),
    path('reviews/create/', views.ReviewCreateView.as_view()),
    path('reviews/<int:pk>/', views.ReviewsDetailView.as_view()),
    path('reviews/<int:pk>/update/', views.ReviewUpdateView.as_view()),


    path('users/<int:pk>/', views.UsersDetailView.as_view()),
    path('users/', views.UsersView.as_view()),


    path('cart/', views.CartView.as_view()),
    path('cart/<int:pk>', views.CartDetailView.as_view()),
    path('cart/create/', views.CartCreateView.as_view()),
    path('cart/<int:pk>/update', views.CartUpdateView.as_view()),

    path('order/', views.OrderView.as_view()),
    path('order/<int:pk>', views.OrderDetailView.as_view()),
    path('order/create/', views.OrderCreateView.as_view()),
    path('order/<int:pk>/update', views.OrderUpdateView.as_view()),


]
