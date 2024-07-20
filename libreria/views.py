from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.files.base import ContentFile
import requests
from io import BytesIO
from django.core.files import File

def register(request):
    if request.method == 'POST':
        form = RegistroClienteOnlineForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # No es necesario crear o actualizar ClienteOnline manualmente
            # porque el RegistroClienteOnlineForm ya lo hace

            return redirect('libreria:home') 
    else:
        form = RegistroClienteOnlineForm()

    return render(request, 'libreria/register.html', {
        'form': form
    })



#Vista para el perfil del usuario
@login_required
def perfil(request):
    perfil_usuario = request.user.perfil
    return render(request, 'perfil.html', {'perfil_usuario': perfil_usuario})




@login_required
def editar_perfil(request):
    perfil_usuario = request.user.perfil
    cambios_guardados = False

    if request.method == 'POST':
        formulario = FormularioPerfil(request.POST, request.FILES, instance=perfil_usuario)
        if formulario.is_valid():
            formulario.save()
            cambios_guardados = True
            return render(request, 'perfil.html', {'formulario': formulario, 'cambios_guardados': cambios_guardados})
    else:
        formulario = FormularioPerfil(instance=perfil_usuario)

    return render(request, 'editar_perfil.html', {'formulario': formulario, 'cambios_guardados': cambios_guardados})





# Vista de la página de inicio, muestra todos los libros
def home(request):
    libros = Libro.objects.all()
    context = {"libros": libros}
    return render(request, 'libreria/home.html', context)



# Vista para la página de índice
def index(request):
    return render(request, 'libreria/index.html')




def acerca_de_mi(request):
    return render(request, 'libreria/acerca_de_mi.html')




def adminlibros(request):
    if request.method == 'POST':
        libro_id = request.POST.get('libro_id')
        try:
            libro = Libro.objects.get(id=libro_id)
            libro.disponible = not libro.disponible
            libro.save()
        except Libro.DoesNotExist:
            pass
        return redirect('libreria:adminlibros')
    
    libros = Libro.objects.all()
    context = {'libros': libros}
    return render(request, 'libreria/adminlibros.html', context)




# Vista para buscar libros, filtra según el título
def buscar_libro_view(request):
    query = request.GET.get('q', '')
    if query:
        libros = Libro.objects.filter(titulo__icontains=query)
    else:
        libros = Libro.objects.all()
        
    deseados_ids = []
    if request.user.is_authenticated:
        deseados_ids = ListaDeseados.objects.filter(usuario=request.user).values_list('libro_id', flat=True)

    return render(request, 'libreria/buscar_libro.html', {
        'libros': libros,
        'query': query,
        'deseados_ids': list(deseados_ids),
    })





def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'libreria/agregar_autor_libro', {'libros': libros})




def detalles_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    return render(request, 'libreria/detalles_libro.html', {'libro': libro})




def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('libreria:adminlibros.html')
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'editar_libro.html', {'form': form, 'libro': libro})




def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('libreria/adminlibros.html') 
    else:
        form = LibroForm()
    
    return render(request, 'libreria/agregar_libro.html', {'form': form})





def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    libro.delete()
    return redirect('libreria:adminlibros')





# Vista para manejar el inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('libreria:home')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    return render(request, 'libreria/login.html', {'form': form})





#vista para el cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('libreria:home')




# Verifica si el usuario es un administrador
def es_admin(user):
    return user.is_authenticated and user.is_superuser



@login_required
@user_passes_test(es_admin)
def vista_restringida_admin(request):
    # Lógica de la vista restringida para administradores
    return render(request, 'ruta/a/template_admin.html')



# Vista para agregar un autor y un libro
def agregar_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('libreria:lista_autores')  
        form = AutorForm()
    
    return render(request, 'agregar_editar_autor.html', {
        'autor_form_title': 'Agregar Autor',
        'autor_form': form
    })




def editar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect('libreria:lista_autores') 
    else:
        form = AutorForm(instance=autor)
    
    return render(request, 'agregar_editar_autor.html', {
        'autor_form_title': 'Editar Autor',
        'autor': autor,
        'autor_form': form
    })





@login_required
def eliminar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    autor.delete()
    return redirect('lista_autores')





# Vista para agregar un cliente
@login_required

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteTiendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('libreria:agregar_cliente')
        else:
            print("Errores en el formulario:", form.errors)
            print("Datos del POST:", request.POST)
    else:
        form = ClienteTiendaForm()

    clientes = ClienteTienda.objects.all()

    return render(request, 'libreria/agregar_cliente.html', {'form': form, 'clientes': clientes})





@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(ClienteTienda, id=id)
    form = ClienteTiendaForm(instance=cliente) 

    if request.method == 'POST':
        if 'editar_cliente' in request.POST:
            form = ClienteTiendaForm(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                return redirect('libreria:agregar_cliente') 
        elif 'eliminar_cliente' in request.POST:
            cliente.delete()
            return redirect('libreria:agregar_cliente')  

    return render(request, 'libreria/editar_cliente.html', {'form': form, 'cliente': cliente})




@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(ClienteTienda, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('libreria:agregar_cliente')  
   
    return redirect('libreria:agregar_cliente')  




# Vista para mostrar y agregar reseñas
def reviews(request):
    reviews = Review.objects.all()
    range_of_stars = range(1, 6)

    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if request.user.is_authenticated:  # Verifica si el usuario está autenticado
            if form.is_valid():
                review = form.save(commit=False)
                review.usuario = request.user  # Asigna el usuario actual
                review.save()
                return redirect('libreria:reviews')
        else:
            messages.error(request, "Debes iniciar sesión para agregar una reseña.")
            return redirect('libreria:login')  # Redirige al login
    else:
        form = ReviewsForm()

    return render(request, 'libreria/reviews.html', {
        'form': form,
        'reviews': reviews,
        'range_of_stars': range_of_stars,
    })




@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.usuario or request.user.is_staff:
        review.delete()
        messages.success(request, "Reseña eliminada correctamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar esta reseña.")
    return redirect('libreria:reviews')




#vista para carrito de compras
def carrito(request):
    carrito = request.session.get('carrito', {})
    libros = Libro.objects.filter(id__in=carrito.keys())
    
    detalles_carrito = []
    total = 0
    
    for libro in libros:
        cantidad = carrito[str(libro.id)]
        subtotal = libro.precio * cantidad
        total += subtotal
        detalles_carrito.append({
            'libro': libro,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })
    
    return render(request, 'libreria/carrito.html', {'detalles_carrito': detalles_carrito, 'total': total})




#vista para agregar un libro al carrito
def agregar_al_carrito(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    carrito = request.session.get('carrito', {})

    if str(libro.id) in carrito:
        carrito[str(libro.id)] += 1
    else:
        carrito[str(libro.id)] = 1

    request.session['carrito'] = carrito

    return redirect('libreria:buscar_libro')




def quitar_del_carrito(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        if str(libro.id) in carrito:
            del carrito[str(libro.id)]
            request.session['carrito'] = carrito
    
    return redirect('libreria:carrito')





@login_required
def checkout(request):
    carrito = request.session.get('carrito', {})
    libros = Libro.objects.filter(id__in=carrito.keys())

    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                cliente_online = ClienteOnline.objects.get(usuario=request.user)
            except ClienteOnline.DoesNotExist:
                return redirect('libreria:register')  # O mostrar un mensaje de error

            total = sum(libro.precio * carrito[str(libro.id)] for libro in libros)
            
            orden = Orden.objects.create(cliente_online=cliente_online, total=total)

            for libro in libros:
                cantidad = carrito[str(libro.id)]
                subtotal = libro.precio * cantidad
                OrdenItem.objects.create(orden=orden, libro=libro, cantidad=cantidad, subtotal=subtotal)
            
            # Limpiar carrito
            request.session['carrito'] = {}

            return redirect('libreria:checkout2')

        else:
            form = ClienteTiendaForm(request.POST)
            if form.is_valid():
                cliente_tienda = form.save()
                total = sum(libro.precio * carrito[str(libro.id)] for libro in libros)
                orden = Orden.objects.create(cliente_tienda=cliente_tienda, total=total)

                for libro in libros:
                    cantidad = carrito[str(libro.id)]
                    subtotal = libro.precio * cantidad
                    OrdenItem.objects.create(orden=orden, libro=libro, cantidad=cantidad, subtotal=subtotal)
                
                request.session['carrito'] = {}
                return redirect('libreria:checkout2')
            else:
                detalles_carrito = []
                total = 0

                for libro in libros:
                    cantidad = carrito[str(libro.id)]
                    subtotal = libro.precio * cantidad
                    total += subtotal
                    detalles_carrito.append({
                        'libro': libro,
                        'cantidad': cantidad,
                        'subtotal': subtotal,
                    })

                return render(request, 'libreria/checkout.html', {'form': form, 'detalles_carrito': detalles_carrito, 'total': total})

    else:
        detalles_carrito = []
        total = 0

        for libro in libros:
            cantidad = carrito[str(libro.id)]
            subtotal = libro.precio * cantidad
            total += subtotal
            detalles_carrito.append({
                'libro': libro,
                'cantidad': cantidad,
                'subtotal': subtotal,
            })

        form = ClienteTiendaForm()

        return render(request, 'libreria/checkout.html', {'form': form, 'detalles_carrito': detalles_carrito, 'total': total})





def checkout2(request):
    return render(request, 'libreria/checkout2.html')






# Añade una lista de libros deseados

@login_required
def lista_deseados(request):
    libros_deseados = ListaDeseados.objects.filter(usuario=request.user)
    
    context = {
        'libros_deseados': libros_deseados
    }
    return render(request, 'libreria/lista_deseados.html', context)




@login_required
def agregar_a_deseados(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    ListaDeseados.objects.get_or_create(usuario=request.user, libro=libro)
    return redirect('libreria:buscar_libro')




@login_required
def quitar_de_deseados(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    ListaDeseados.objects.filter(usuario=request.user, libro=libro).delete()
    return redirect('libreria:buscar_libro')
