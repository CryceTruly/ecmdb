from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="reports"),
    path('add-report', views.add_report, name="add_report")
]
