from django.urls import path
from .views import (
    TodoCreateView,
    TodoListView,
    TodoDetailView,
    TodoUpdateView,
    TodoDeleteView,
)

urlpatterns = [
    path("new/", TodoCreateView.as_view(), name="todo_new"),
    path("<int:pk>/", TodoDetailView.as_view(), name="todo_detail"),
    path("", TodoListView.as_view(), name="todo_list"),
    path("<int:pk>/edit/", TodoUpdateView.as_view(), name="todo_edit"),
    path("<int:pk>/confirm-delete/", TodoDeleteView.as_view(), name="todo_delete"),
]
