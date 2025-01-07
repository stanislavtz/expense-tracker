from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<int:expense_id>", views.edit_expense, name="edit"),
]
