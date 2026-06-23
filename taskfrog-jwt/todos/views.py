from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import Todo

# Create your views here.


class TodoCreateView(CreateView):
    model = Todo
    template_name = "todos/todo_new.html"
    fields = ["title", "body"]
    success_url = reverse_lazy("todo_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoListView(ListView):
    model = Todo
    template_name = "todos/todo_list.html"


class TodoDetailView(DetailView):
    model = Todo
    template_name = "todos/todo_detail.html"


class TodoUpdateView(UpdateView):
    model = Todo
    template_name = "todos/todo_edit.html"
    fields = ["title", "body"]


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = "todos/todo_delete.html"
    success_url = reverse_lazy("todo_list")
