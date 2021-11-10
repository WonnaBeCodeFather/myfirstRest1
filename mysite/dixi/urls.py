from django.urls import path

from . import views

urlpatterns = [
    path('product/', views.ProductListView.as_view()),
    path('product/<int:pk>/', views.ProductDetailView.as_view()),
    path('reviews/', views.ReviewsView.as_view()),
    path('reviews/create/', views.ReviewCreateView.as_view()),
    path('reviews/<int:pk>/', views.ReviewsDetailView.as_view()),
    path('reviews/<int:pk>/update/', views.ReviewUpdateView.as_view()),

]
