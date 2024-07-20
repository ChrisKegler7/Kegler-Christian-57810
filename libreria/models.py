from django import forms
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.signals import post_save
from django.dispatch import receiver

class Autor(models.Model):
    nombre = models.CharField(max_length=100)



class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()
    isbn = models.CharField(max_length=13)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    sinopsis = models.TextField(default='Sin sinopsis')
    imagen = models.ImageField(upload_to='libros/', null=True, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
    )
    direccion = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'direccion']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            direccion = self.cleaned_data.get('direccion')
            ClienteOnline.objects.create(
                usuario=user,
                direccion=direccion
            )
        return user



class Review(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='reseñas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'Reseña de "{self.libro.titulo}" por {self.usuario.username}'
    



class ClienteTienda(models.Model):
    nombre = models.CharField(max_length=200)
    correo_electronico = models.EmailField(max_length=200)
    direccion = models.CharField(max_length=300)
    libros_comprados = models.ManyToManyField(Libro, through='Compra')

    def __str__(self):
        return self.nombre




class ClienteOnline(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=300)

    def __str__(self):
        return self.usuario.username





class Compra(models.Model):
    cliente = models.ForeignKey(ClienteTienda, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cliente.nombre} - {self.libro.titulo} ({self.cantidad} unidades)'




class Orden(models.Model):
    cliente_online = models.ForeignKey(ClienteOnline, null=True, blank=True, on_delete=models.CASCADE)
    cliente_tienda = models.ForeignKey(ClienteTienda, null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_orden = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.cliente_online:
            return f'Orden de {self.cliente_online.usuario.username}'
        elif self.cliente_tienda:
            return f'Orden de {self.cliente_tienda.nombre}'
        return 'Orden sin cliente'




class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.libro.titulo} - {self.cantidad} unidades'
    



class ListaDeseados(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    añadido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'libro')




class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    else:
        instance.perfil.save()
