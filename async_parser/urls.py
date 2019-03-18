from django.urls import path, include
from .views import retry_file, create_task

urlpatterns = [
    path('retry-file/<int:file_id>/', retry_file),
    path('create-task/', create_task),
]
