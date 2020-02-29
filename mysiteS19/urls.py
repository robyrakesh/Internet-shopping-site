from django.contrib import admin
from django.urls import include, path
from mysiteS19 import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
]
