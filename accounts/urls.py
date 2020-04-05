from django.urls import path
from . import views


urlpatterns = [
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
]

# path("accounts", views.accounts, name="accounts"),
# path("technician", views.technician, name="technician"),
# path("boss", views.boss, name="boss")
