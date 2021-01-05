from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from . import views

app_name = "pos"

urlpatterns = [
    path('', views.index, name="index"),
    path('pos/index', views.pos_index, name="pos_index"),
    path('pos/add-supply/', views.add_supply, name="add_supply"),
    path('pos/add-product/', views.add_product, name="add_product"),
    path('pos/add-purchase/', views.add_purchase, name="add_purchase"),
    path('pos/add-expenses/', views.add_expense, name="add_expense"),
    path('pos/history/', views.history, name="history"),
    path('pos/history/<int:year>/', views.history, name="history"),
    path('pos/history/<int:year>/<int:month>/', views.history, name="history"),
    path('pos/history/<int:year>/<int:month>/<int:day>/', views.history, name="history"),
    path('pos/drug/history/', views.drug_history, name="drug_history"),
    path('pos/drug/history/<drug>/', views.drug_history, name="drug_history"),
    path('pos/supply/history/', views.supply_history, name="supply_history"),
    path('pos/login/', LoginView.as_view(), name="login"),
    path('pos/logout/', LogoutView.as_view(), name="logout"),
    path('pos/admin/', admin.site.urls, name='admin'),
    path('pos/items_list/', views.items_list, name="items_list"),
    path('pos/history/page', views.history_page, name="history_page"),
    path('pos/statistics', views.statistics, name="statistics"),

]