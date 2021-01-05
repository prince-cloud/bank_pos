from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from . import views

app_name = "bank"

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('bank/index', views.bank_index, name="bank_index"),
    path('bank/account/registration', views.register, name="bank_register_account"),
    path('bank/account/edit/<int:pk>/', views.edit_profile, name="edit_profile"),
    path('bank/account/delete/<int:pk>/', views.delete_account, name="delete_account"),
    path('bank/deposite/to/<int:pk>/', views.deposite, name="deposite"),
    path('bank/withdraw/from/<int:pk>/', views.withdrawal, name="withdrawal"),
    path('bank/profile/<int:pk>/', views.profile, name="profile"),

    path('bank/profile/transactions/<int:pk>/', views.transactions, name="transactions"),
    path('bank/profile/transactions/<int:pk>/<int:year>/', views.transactions, name="transactions"),
    path('bank/profile/transactions/<int:pk>/<int:year>/<int:month>/', views.transactions, name="transactions"),
    path('bank/profile/transactions/<int:pk>/<int:year>/<int:month>/<int:day>/', views.transactions, name="transactions"),
]