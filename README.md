# Kegler-Christian-57810
 
 # link del video: https://youtu.be/mqHmDHu6pjw

# Nombre del Proyecto

Proyecto Final coderhouse comision 57810

## Descripción

Este proyecto es una página web para una librería que combina la venta de libros en línea con la posibilidad de dejar comentarios sobre los libros. La plataforma permite a los usuarios explorar una amplia gama de libros, agregarlos a un carrito de compras y realizar pedidos en línea. Además, los usuarios pueden dejar reseñas para compartir sus opiniones sobre los libros que han leído.

La librería también cuenta con una tienda física, proporcionando una experiencia completa tanto para los compradores en línea como para los clientes que prefieren visitar el establecimiento. 

## Funcionalidades Clave

- **Venta en Línea:** Navega, selecciona y compra libros en línea.
- **Reseñas de Libros:** Los usuarios pueden dejar reseñas y calificaciones para los libros.
- **Tienda Física:** Información sobre la tienda física y su ubicación.
- **Carrito de Compras:** Añade libros a tu carrito y realiza el pago en línea.
- **Wishlist:** Guarda tus libros favoritos en una lista de deseos.
- **Perfil de Usuario:** Gestiona tu perfil y visualiza tu historial de compras.


## Usuario administrador 

user: admin
pass: administrador


## Descripción de Modelos

A continuación se describe la estructura de los modelos utilizados en el proyecto:

### Autor

Representa a un autor de libros.

- **nombre**: Nombre del autor (Campo de texto, máximo 100 caracteres).

### Libro

Representa un libro disponible en la librería.

- **titulo**: Título del libro (Campo de texto, máximo 200 caracteres).
- **autor**: Relación con el modelo `Autor` (Clave foránea).
- **fecha_publicacion**: Fecha de publicación del libro.
- **isbn**: ISBN del libro (Campo de texto, máximo 13 caracteres).
- **precio**: Precio del libro (Decimal con 2 decimales).
- **sinopsis**: Sinopsis del libro (Campo de texto, valor predeterminado 'Sin sinopsis').
- **imagen**: Imagen del libro (Campo de imagen, opcional).
- **disponible**: Disponibilidad del libro (Campo booleano).

### CustomUserCreationForm

Formulario personalizado para la creación de usuarios, extendiendo `UserCreationForm`.

- **email**: Correo electrónico del usuario.
- **password1**: Contraseña del usuario.
- **password2**: Confirmación de la contraseña.
- **direccion**: Dirección del usuario.

### Review

Representa una reseña hecha por un usuario sobre un libro.

- **libro**: Relación con el modelo `Libro` (Clave foránea).
- **usuario**: Relación con el modelo `User` (Clave foránea).
- **comentario**: Comentario del usuario (Campo de texto).
- **calificacion**: Calificación del libro (Entero, entre 1 y 5).

### ClienteTienda

Representa un cliente que compra en la tienda física.

- **nombre**: Nombre del cliente (Campo de texto, máximo 200 caracteres).
- **correo_electronico**: Correo electrónico del cliente (Campo de texto, máximo 200 caracteres).
- **direccion**: Dirección del cliente (Campo de texto, máximo 300 caracteres).
- **libros_comprados**: Relación con el modelo `Libro` a través del modelo `Compra`.

### ClienteOnline

Representa un cliente que compra en línea.

- **usuario**: Relación con el modelo `User` (Clave foránea).
- **direccion**: Dirección del cliente en línea (Campo de texto, máximo 300 caracteres).

### Compra

Representa una compra realizada por un cliente en la tienda física.

- **cliente**: Relación con el modelo `ClienteTienda` (Clave foránea).
- **libro**: Relación con el modelo `Libro` (Clave foránea).
- **cantidad**: Cantidad de libros comprados (Número entero positivo).
- **subtotal**: Subtotal de la compra (Decimal con 2 decimales).
- **fecha_compra**: Fecha y hora de la compra.

### Orden

Representa una orden de compra, ya sea en línea o en la tienda física.

- **cliente_online**: Relación con el modelo `ClienteOnline` 
- **cliente_tienda**: Relación con el modelo `ClienteTienda`
- **total**: Total de la orden (Decimal con 2 decimales).
- **fecha_orden**: Fecha y hora de la orden.

### OrdenItem

Representa un ítem en una orden.

- **orden**: Relación con el modelo `Orden`
- **libro**: Relación con el modelo `Libro` 
- **cantidad**: Cantidad del libro en la orden (Número entero positivo).
- **subtotal**: Subtotal del ítem (Decimal con 2 decimales).

### ListaDeseados

Representa una lista de deseos de un usuario.

- **usuario**: Relación con el modelo `User`
- **libro**: Relación con el modelo `Libro` 
- **añadido_en**: Fecha y hora en que el libro fue añadido a la lista de deseos.

### Perfil

Representa el perfil de un usuario.

- **user**: Relación con el modelo `User` 
- **biografia**: Biografía del usuario (Campo de texto, opcional).
- **ubicacion**: Ubicación del usuario (Campo de texto, opcional, máximo 100 caracteres).
- **fecha_nacimiento**: Fecha de nacimiento del usuario (Fecha, opcional).
- **avatar**: Imagen de perfil del usuario (Campo de imagen, opcional).

### Señales

- **crear_o_actualizar_perfil**: Señal que crea o actualiza el perfil del usuario cuando se guarda un `User`.

## Cómo Ejecutar el Proyecto

1. Clonar el repositorio.
2. Instalar las dependencias: `pip install -r requirements.txt`
3. Aplicar las migraciones: `python manage.py migrate`
4. Ejecutar el servidor: `python manage.py runserver`
