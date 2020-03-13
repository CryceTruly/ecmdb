from django.urls import path
from . import views


urlpatterns = [
    path("", views.expenses, name="expenses"),
    path("expenses_add", views.expenses_add, name="expenses_add"),
    path("expense_detail", views.expense_detail, name="expense_detail"),
    path("expense_edit/<int:id>", views.expense_edit, name="expense_edit"),
    path("expense_delete", views.expense_delete, name="expense_delete"),
]
