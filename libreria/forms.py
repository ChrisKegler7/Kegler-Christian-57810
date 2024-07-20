from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm



class CustomDateInput(forms.DateInput):
    input_type = 'text'



class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre']



class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'fecha_publicacion', 'isbn', 'precio', 'sinopsis', 'imagen']




class ClienteTiendaForm(forms.ModelForm):
    class Meta:
        model = ClienteTienda
        fields = ['nombre', 'correo_electronico', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }




class RegistroClienteOnlineForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        required=True
    )
    direccion = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            ClienteOnline.objects.create(
                usuario=user,
                direccion=self.cleaned_data['direccion']
            )
        return user




class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Review 
        fields = ['libro', 'comentario', 'calificacion']




class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }




class FormularioPerfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['biografia', 'ubicacion', 'fecha_nacimiento', 'avatar']
        widgets = {
            'biografia': forms.Textarea(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }



