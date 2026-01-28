from django.db import models
from django.contrib.auth.models import User

# --- ESTO NO LO TOQUES (Es tu tarea actual) ---
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title +'- by '+ self.user.username

# --- AQUÍ EMPIEZA LO NUEVO (Quita los # desde aquí para abajo) ---

class DatosPersonales(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    descripcionperfil = models.TextField(max_length=500)
    nacionalidad = models.CharField(max_length=20)
    fechanacimiento = models.DateField()
    numerocedula = models.CharField(max_length=10, unique=True)
    sexo = models.CharField(max_length=1, choices=[('H', 'Hombre'), ('M', 'Mujer')])
    telefonofijo = models.CharField(max_length=15, blank=True)
    direcciondomiciliaria = models.CharField(max_length=100)
    sitioweb = models.URLField(blank=True)
    archivo_cv_pdf = models.FileField(upload_to='cvs/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='experiencias')
    nombrempresa = models.CharField(max_length=100)
    cargodesempenado = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    logros = models.TextField()

    def __str__(self):
        return f"{self.cargodesempenado} en {self.nombrempresa}"

class Habilidad(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='habilidades')
    nombre = models.CharField(max_length=50)
    nivel = models.PositiveIntegerField(default=50) 
    porcentaje = models.IntegerField(default=50, verbose_name="Nivel (0-100)")
    descripcion = models.TextField(verbose_name="Contexto Corto", blank=True, null=True, help_text="Ej: Uso avanzado para Data Science.")
    def __str__(self):
        return self.nombre
    # --- Pégalo al final de models.py ---

class Reconocimiento(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, verbose_name="Título del Certificado")
    institucion = models.CharField(max_length=100, verbose_name="Institución")
    # Usaremos ImageField para que puedas subir la foto real desde el admin
    imagen = models.ImageField(upload_to='certificados/', verbose_name="Foto del Título", null=True, blank=True)

    def __str__(self):
        return self.titulo
    # --- Pégalo al final de models.py ---

class Educacion(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, verbose_name="Título Obtenido")
    institucion = models.CharField(max_length=100, verbose_name="Institución Educativa")
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha Inicio")
    fecha_fin = models.DateField(null=True, blank=True, verbose_name="Fecha Fin (Dejar vacío si cursas actualmente)")
    
    def __str__(self):
        return self.titulo
    # --- AL FINAL DE models.py ---

class ProductoGarage(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción", blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio ($)")
    imagen = models.ImageField(upload_to='garage/', verbose_name="Foto del Producto")
    stock = models.IntegerField(default=1, verbose_name="Cantidad Disponible")

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
    # --- AL FINAL DE models.py ---

class RecursoAcademico(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, verbose_name="Área (ej. Backend)")
    descripcion = models.TextField(verbose_name="Tecnologías (ej. Django, APIs)")
    icono = models.CharField(max_length=50, default="fas fa-book", verbose_name="Icono FontAwesome (ej. fab fa-python)")
    def __str__(self):
        return self.titulo