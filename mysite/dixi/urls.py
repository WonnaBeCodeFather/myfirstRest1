from django.urls import path

from . import  views

urlpatterns = [
    path('product/', views.ProductListView.as_view()),
    path('product/<int:pk>/', views.ProductDetailView.as_view()),
    path('reviews/', views.ReviewsCreateView.as_view()),
    path('reviews/<int:pk>/', views.ReviewsDetailView.as_view()),

]
