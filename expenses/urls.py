from django.urls import path
from . import views


urlpatterns = [
    path("", views.expenses, name="expenses"),
    path("expenses_add", views.expenses_add, name="expenses_add"),
    path("expense_detail", views.expense_detail, name="expense_detail"),
    path("summary", views.expense_summary, name="summary"),
    path("expense_edit/<int:id>", views.expense_edit, name="expense_edit"),
    path("approve_expense/<int:id>", views.approve_expense, name="approve_expense"),
    path("expense_delete", views.expense_delete, name="expense_delete"),
    path('expenses/search_expenses', views.search_expenses, name='search_expenses'),
    path('expenses/summary_rest', views.expense_summary_rest,
         name='expenses_summary_rest'),

    path('expenses/todays-expense-export/<period>',
         views.today_expense_export, name='todays-expense-export')
]
