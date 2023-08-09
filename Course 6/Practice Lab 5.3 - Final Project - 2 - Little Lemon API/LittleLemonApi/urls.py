from django.urls import path
from . import views


urlpatterns = [
    path('menu-items/', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>/', views.SingleItemView.as_view()),
    path('groups/manager/users/', views.UsersView.as_view()),
    path('groups/manager/users/<int:pk>/', views.SingleUserView.as_view()),
    path('groups/delivery-crew/users/', views.crewView.as_view()),
    path('groups/delivery-crew/users/<int:pk>/', views.crewSingleView.as_view()),
    path('cart/menu-items/', views.customerCartView.as_view()),
    path('orders/', views.ordersView.as_view()),
    path('orders/<int:pk>/', views.singleOrderView.as_view()),

]
