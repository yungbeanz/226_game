from django.urls import path
from . import views

from django.contrib import admin
from dejango.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/', include('game.urls')),
]