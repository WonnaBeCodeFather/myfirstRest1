from django.urls import path

from . import views

urlpatterns = [
    path('category/create', views.CategoryCreateView.as_view()),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view()),
    path('material/create', views.MaterialCreateView.as_view()),
    #path('product/create', views.ProductCreateView.as_view()),
    path('product/<int:pk>/update', views.ProductUpdateView.as_view()),
    path('size/create', views.SizeCreateView.as_view()),
    path('size/<int:pk>/', views.SizeUpdateView.as_view()),
    #path('price/create', views.PriceCreateView.as_view()),
    path('price/<int:pk>/update', views.PriceUpdateView.as_view()),
    path('product/', views.ProductListView.as_view()),
    path('product/<slug:slug>/', views.ProductDetailView.as_view()),
    path('superview/', views.SuperView.as_view()),


    path('reviews/create/', views.ReviewCreateView.as_view()),
    path('reviews/<int:pk>/update/', views.ReviewUpdateView.as_view()),
    path('reviews/', views.ReviewsView.as_view()),
    path('reviews/<int:pk>/', views.ReviewsDetailView.as_view()),


    path('users/<int:pk>/', views.UsersDetailView.as_view()),
    path('users/', views.UsersView.as_view()),


    path('cart/create/', views.CartCreateView.as_view()),
    path('cart/<int:pk>/update', views.CartUpdateView.as_view()),
    path('cart/', views.CartView.as_view()),
    path('cart/<int:pk>', views.CartDetailView.as_view()),


    path('order/create/', views.OrderCreateView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('order/<int:pk>', views.OrderDetailView.as_view()),
    path('order/<int:pk>/update', views.OrderUpdateView.as_view()),

    path('gallery/create/', views.GalleryCreateView.as_view()),
]
