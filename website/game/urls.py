from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('greet/<str:name>', views.greet, name='greet'),
    path('create', views.create, name='create'),
    path('pick/<str:player>/<str:x>/<str:y>', views.pick, name='pick'),
]
