from django.urls import path  
from . import views

app_name = 'main' 

urlpatterns = [
	path('',views.index,name='index'),
	path('list/',views.list,name='list'),
	path('product/<int:pid>',views.product,name='product'),
]