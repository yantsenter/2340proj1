from django.urls import path, include
from . import views
from .views import update_password_view

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path("update-password/", views.update_password_view, name="accounts.update_password"),
]