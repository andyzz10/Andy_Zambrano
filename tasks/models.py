from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date

# --- MODELO DE TAREAS ---
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #validacionfechanacimiento
    

    def __str__(self):
        return self.title + ' - by ' + self.user.username

# --- DATOS PERSONALES ---
class DatosPersonales(models.Model):
    solo_numeros = RegexValidator(r'^\d+$', 'Solo se permiten números (0-9).')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    descripcionperfil = models.TextField(max_length=500)
    nacionalidad = models.CharField(max_length=20, default="Ecuatoriana")
    fechanacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    numerocedula = models.CharField(max_length=10, unique=True, validators=[solo_numeros], verbose_name="Cédula")
    sexo = models.CharField(max_length=1, choices=[('H', 'Hombre'), ('M', 'Mujer')])
    
    ESTADO_CIVIL_CHOICES = [('Soltero/a', 'Soltero/a'), ('Casado/a', 'Casado/a'), ('Divorciado/a', 'Divorciado/a'), ('Viudo/a', 'Viudo/a'), ('Unión Libre', 'Unión Libre')]
    estadocivil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, default="Soltero/a", verbose_name="Estado Civil")
    
    LICENCIA_CHOICES = [('A', 'Tipo A (Motos)'), ('B', 'Tipo B (Autos)'), ('C', 'Tipo C (Taxis)'), ('D', 'Tipo D (Bus)'), ('E', 'Tipo E (Pesados)'), ('F', 'Tipo F (Especiales)'), ('G', 'Tipo G (Maquinaria)')]
    licenciaconducir = models.CharField(max_length=5, choices=LICENCIA_CHOICES, blank=True, null=True, verbose_name="Licencia de Conducir")
    
    telefonofijo = models.CharField(max_length=15, blank=True, validators=[solo_numeros], verbose_name="Celular/Fijo")
    telefonoconvencional = models.CharField(max_length=15, blank=True, null=True, validators=[solo_numeros], verbose_name="Tel. Convencional")
    direcciondomiciliaria = models.CharField(max_length=100, verbose_name="Domicilio")
    direcciontrabajo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dirección Trabajo")
    sitioweb = models.URLField(blank=True, verbose_name="Sitio Web")
    
    # --- CONFIGURACIÓN DE VISIBILIDAD ---
    mostrar_experiencia = models.BooleanField(default=True, verbose_name="Mostrar Pestaña Experiencia")
    mostrar_productos_laborales = models.BooleanField(default=True, verbose_name="Mostrar Pestaña Productos Laborales") 
    mostrar_reconocimientos = models.BooleanField(default=True, verbose_name="Mostrar Pestaña Certificados")
    mostrar_cursos = models.BooleanField(default=True, verbose_name="Mostrar Pestaña Cursos") 
    mostrar_productos_academicos = models.BooleanField(default=True, verbose_name="Mostrar Pestaña Productos Académicos") 
    mostrar_garage = models.BooleanField(default=True, verbose_name="Mostrar Botón Venta Garage")

    mostrar_botones = models.BooleanField(default=True, verbose_name="Mostrar Botones Superiores")
    foto_portada = models.ImageField(upload_to='portadas/', verbose_name="Foto de Portada", blank=True, null=True)
#ValidacionFechaNacimiento
    # ... (tus campos anteriores: mostrar_garage, foto_portada, etc.) ...

    def clean(self):
        # Validación: Fecha de nacimiento no puede ser futura
        if self.fechanacimiento and self.fechanacimiento > date.today():
            raise ValidationError({'fechanacimiento': "⛔ Error: ¡No puedes nacer en el futuro! Ingresa una fecha válida."})

    def save(self, *args, **kwargs):
        self.full_clean() # Esto obliga a ejecutar la validación antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# --- EXPERIENCIA LABORAL ---
class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='experiencias')
    cargodesempenado = models.CharField(max_length=100, verbose_name="Cargo Desempeñado")
    nombrempresa = models.CharField(max_length=50, verbose_name="Nombre de la Empresa")
    lugarempresa = models.CharField(max_length=50, verbose_name="Lugar/Ciudad", blank=True, null=True)
    emailempresa = models.EmailField(max_length=100, verbose_name="Email Empresa", blank=True, null=True)
    sitiowebempresa = models.URLField(max_length=100, verbose_name="Sitio Web Empresa", blank=True, null=True)
    nombrecontactoempresarial = models.CharField(max_length=100, verbose_name="Nombre Contacto", blank=True, null=True)
    telefonocontactoempresarial = models.CharField(max_length=60, verbose_name="Teléfono Contacto", blank=True, null=True)
    fechainiciogestion = models.DateField(verbose_name="Fecha Inicio")
    fechafingestion = models.DateField(verbose_name="Fecha Fin", null=True, blank=True)
    descripcionfunciones = models.TextField(verbose_name="Descripción de Funciones/Logros", max_length=500, default="Pendiente de llenar")
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en la Web")
    rutacertificado = models.ImageField(upload_to='certificados_laborales/', verbose_name="Certificado Laboral", blank=True, null=True)

    def __str__(self):
        return f"{self.cargodesempenado} en {self.nombrempresa}"
    def clean(self):
        if self.fechafingestion and self.fechainiciogestion and self.fechafingestion < self.fechainiciogestion:
            raise ValidationError("⛔ Error: La fecha de fin no puede ser anterior a la de inicio.")
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# --- CURSOS REALIZADOS ---
class CursoRealizado(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='cursos')
    nombrecurso = models.CharField(max_length=100, verbose_name="Nombre del Curso")
    fechainicio = models.DateField(verbose_name="Fecha Inicio")
    fechafin = models.DateField(verbose_name="Fecha Fin")
    totalhoras = models.IntegerField(verbose_name="Total Horas")
    descripcioncurso = models.CharField(max_length=100, verbose_name="Descripción del Curso")
    entidadpatrocinadora = models.CharField(max_length=100, verbose_name="Entidad Patrocinadora")
    nombrecontactoauspicia = models.CharField(max_length=100, verbose_name="Nombre Contacto", blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, verbose_name="Teléfono Contacto", blank=True, null=True)
    emailempresapatrocinadora = models.CharField(max_length=60, verbose_name="Email Empresa", blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en la Web")
    rutacertificado = models.ImageField(upload_to='certificados_cursos/', verbose_name="Certificado", blank=True, null=True)
    def __str__(self):
        return self.nombrecurso

# --- RECONOCIMIENTOS ---
class Reconocimiento(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    TIPO_CHOICES = [('Académico', 'Académico'), ('Público', 'Público'), ('Privado', 'Privado')]
    tiporeconocimiento = models.CharField(max_length=100, choices=TIPO_CHOICES, verbose_name="Tipo de Reconocimiento")
    descripcionreconocimiento = models.CharField(max_length=100, verbose_name="Nombre del Reconocimiento")
    entidadpatrocinadora = models.CharField(max_length=100, verbose_name="Entidad/Institución")
    fechareconocimiento = models.DateField(verbose_name="Fecha")
    nombrecontactoauspicia = models.CharField(max_length=100, verbose_name="Nombre Contacto", blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, verbose_name="Teléfono Contacto", blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en la Web")
    rutacertificado = models.ImageField(upload_to='certificados/', verbose_name="Imagen del Certificado", null=True, blank=True)
    def __str__(self):
        return f"{self.descripcionreconocimiento} - {self.entidadpatrocinadora}"

# --- PRODUCTOS ACADEMICOS ---
class ProductoAcademico(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombrerecurso = models.CharField(max_length=100, verbose_name="Nombre del Recurso")
    clasificador = models.CharField(max_length=100, verbose_name="Clasificador")
    descripcion = models.CharField(max_length=100, verbose_name="Descripción") 
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en la Web")
    def __str__(self):
        return self.nombrerecurso

# --- PRODUCTOS LABORALES ---
class ProductoLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombreproducto = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    fechaproducto = models.DateField(verbose_name="Fecha")
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en la Web")
    def __str__(self):
        return self.nombreproducto

# --- VENTA GARAGE (NUEVO MODELO - REEMPLAZA A ProductoGarage) ---
class VentaGarage(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='ventas_garage')
    nombreproducto = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    
    ESTADO_CHOICES = [('Bueno', 'Bueno'), ('Regular', 'Regular')]
    estadoproducto = models.CharField(max_length=40, choices=ESTADO_CHOICES, verbose_name="Estado")
    
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")
    valordelbien = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Valor del Bien ($)")
    
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en la Web")
    
    # Campo de imagen (Mantenido para que la web se vea bien)
    imagen = models.ImageField(upload_to='garage/', verbose_name="Foto del Producto", blank=True, null=True)

    def __str__(self):
        return f"{self.nombreproducto} - ${self.valordelbien}"