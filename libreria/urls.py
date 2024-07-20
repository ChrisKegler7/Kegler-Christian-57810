from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'libreria'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('acerca_de_mi/', views.acerca_de_mi, name='acerca_de_mi'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('adminlibros/', views.adminlibros, name='adminlibros'),
    path('agregar_libro/<int:pk>/', views.editar_autor, name='agregar_libro'),
    path('libro/editar/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('libro/eliminar/<int:pk>/', views.eliminar_libro, name='eliminar_libro'),
    path('agregar_autor/<int:pk>/', views.editar_autor, name='agregar_autor'),
    path('editar_autor/<int:pk>/', views.editar_autor, name='editar_autor'),
    path('eliminar_autor/<int:pk>/', views.eliminar_autor, name='eliminar_autor'),
    path('buscar_libro/', views.buscar_libro_view, name='buscar_libro'),
    path('agregar_cliente/', views.agregar_cliente, name='agregar_cliente'),
    path('editar_cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar_cliente/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('agregar_al_carrito/<int:libro_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/quitar/<int:libro_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('detalles_libro/<int:libro_id>/', views.detalles_libro, name='detalles_libro'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('carrito/', views.carrito, name='carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout2/', views.checkout2, name='checkout2'),
    path('deseados/', views.lista_deseados, name='lista_deseados'),    
    path('deseados/agregar/<int:libro_id>/', views.agregar_a_deseados, name='agregar_a_deseados'),
    path('deseados/quitar/<int:libro_id>/', views.quitar_de_deseados, name='quitar_de_deseados'),
]
