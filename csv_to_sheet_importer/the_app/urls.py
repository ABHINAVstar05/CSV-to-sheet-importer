from django.urls import path
from . import views


urlpatterns = [
    path('', views.upload_csv, name = "upload .csv file(s)"),
    path('filter/<str:file_name>/', views.filter, name = "filter csv"),
]