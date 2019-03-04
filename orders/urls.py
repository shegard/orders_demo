from django.urls import path
from . import views

urlpatterns = [

    path('', views.ToOrderView.as_view()),

    path('order/', views.OrderView.as_view()),
    path('item/', views.ItemView.as_view()),

    path('orders/', views.OrderListView.as_view()),
    path('items/', views.OrderItemListView.as_view()),
]
