# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django import forms
from django.urls import path

# Models
class Task(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    due_date = models.DateField(null=True, blank=True)
    tags = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

# Forms
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'tags']

# Views
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_detail.html', {'task': task})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})

# URLs
urlpatterns = [
    path('', task_list, name='task_list'),
    path('task/<int:pk>/', task_detail, name='task_detail'),
    path('task/new/', task_create, name='task_create'),
    path('task/<int:pk>/edit/', task_update, name='task_update'),
    path('task/<int:pk>/delete/', task_delete, name='task_delete'),
]

# Templates
task_list_html = """
{% extends 'base_generic.html' %}
{% block content %}
  <h1>Tasks</h1>
  <ul>
    {% for task in tasks %}
      <li>
        <a href="{% url 'task_detail' task.pk %}">{{ task.title }}</a>
      </li>
    {% endfor %}
  </ul>
  <a href="{% url 'task_create' %}">Add new task</a>
{% endblock %}
"""

task_detail_html = """
{% extends 'base_generic.html' %}
{% block content %}
  <h1>{{ task.title }}</h1>
  <p>{{ task.description }}</p>
  <p>Due: {{ task.due_date }}</p>
  <p>Tags: {{ task.tags }}</p>
  <a href="{% url 'task_update' task.pk %}">Edit</a>
  <form method="post" action="{% url 'task_delete' task.pk %}">
    {% csrf_token %}
    <button type="submit">Delete</button>
  </form>
  <a href="{% url 'task_list' %}">Back to list</a>
{% endblock %}
"""

task_form_html = """
{% extends 'base_generic.html' %}
{% block content %}
  <h1>{% if form.instance.pk %}Edit{% else %}New{% endif %} Task</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">{% if form.instance.pk %}Save{% else %}Create{% endif %}</button>
  </form>
  <a href="{% url 'task_list' %}">Back to list</a>
{% endblock %}
"""

task_confirm_delete_html = """
{% extends 'base_generic.html' %}
{% block content %}
  <h1>Delete Task</h1>
  <p>Are you sure you want to delete "{{ task.title }}"?</p>
  <form method="post">
    {% csrf_token %}
    <button type="submit">Yes, delete</button>
  </form>
  <a href="{% url 'task_list' %}">Back to list</a>
{% endblock %}
"""
