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

    def __str__(self):
        return self.nombre