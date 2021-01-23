from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from . import views

app_name = "pos"

urlpatterns = [
    path('', views.index, name="index"),
    path('pos/login/', LoginView.as_view(), name="login"),
    path('pos/logout/', LogoutView.as_view(), name="logout"),
    path('pos/admin/', admin.site.urls, name='admin'),
    path('pos/index/', views.pos_index, name='pos_index'),
    path('pos/products/list/', views.products_list, name='products_list'),
    path('pos/products/add_purchase/', views.add_purchase, name='add_purchase'),
    path('pos/products/add_supply/', views.add_supply, name='add_supply'),
    path('pos/products/add/product/', views.add_product, name='add_product'),
    path('pos/products/add/expenses/', views.add_expense, name='add_expense'),
    path('pos/history/', views.history, name='history'),
    path('pos/history/supply', views.supply_history, name='supply_history'),

    path('pos/sales_?expenses/', views.sales_expenses, name="sales_expenses"),
    path('pos/sales_?expenses/<int:year>/', views.sales_expenses, name="sales_expenses"),
    path('pos/sales_?expenses/<int:year>/<int:month>/', views.sales_expenses, name="sales_expenses"),
    path('pos/sales_?expenses/<int:year>/<int:month>/<int:day>/', views.sales_expenses, name="sales_expenses"),

    path('pos/statistics/', views.statistics, name="statistics"),

]