from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    # path('', views.home, name='Home'),
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('products', views.products, name='products'),
    path('products/<prod_id>',views.productdetail,name='productdetail'),
    path('placeorder/<prod_id>', views.place_order, name='placeorder'),
    path('login/',views.login,name='login'),
    path('login/user_login',views.user_login,name='userlogin'),
    path('myorders',views.myorders,name='myorders'),
    path('logout',views.user_logout,name='userlogout'),
    path('detail/<int:cat_id>',views.detail,name='detail'),
    path('register',views.register,name='register'),
    ]
