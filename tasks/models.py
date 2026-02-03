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

    # Validación de Fecha de Nacimiento
    def clean(self):
        # 1. No Futuro
        if self.fechanacimiento and self.fechanacimiento > date.today():
            raise ValidationError({'fechanacimiento': "⛔ Error: ¡No puedes nacer en el futuro! Ingresa una fecha válida."})
        # 2. Mínimo 2005
        if self.fechanacimiento and self.fechanacimiento < date(2005, 1, 1):
            raise ValidationError({'fechanacimiento': "⛔ Error: La fecha no puede ser anterior al año 2005."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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

    # --- VALIDACIÓN DE FECHAS EN EXPERIENCIA ---
    def clean(self):
        # Validar Inicio (No futuro y > 2005)
        if self.fechainiciogestion:
            if self.fechainiciogestion > date.today():
                raise ValidationError({'fechainiciogestion': "⛔ Error: La fecha de inicio no puede ser futura."})
            if self.fechainiciogestion < date(2005, 1, 1):
                raise ValidationError({'fechainiciogestion': "⛔ Error: La fecha de inicio no puede ser anterior a 2005."})

        # Validar Fin (No futuro y > 2005)
        if self.fechafingestion:
            if self.fechafingestion > date.today():
                raise ValidationError({'fechafingestion': "⛔ Error: La fecha de fin no puede ser futura."})
            if self.fechafingestion < date(2005, 1, 1):
                raise ValidationError({'fechafingestion': "⛔ Error: La fecha de fin no puede ser anterior a 2005."})

        # Validar coherencia
        if self.fechafingestion and self.fechainiciogestion and self.fechafingestion < self.fechainiciogestion:
            raise ValidationError("⛔ Error Lógico: Terminaste el trabajo antes de empezarlo. Revisa las fechas.")

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

    # --- VALIDACIÓN DE FECHAS EN CURSOS ---
    def clean(self):
        # Validar Inicio
        if self.fechainicio:
            if self.fechainicio > date.today():
                raise ValidationError({'fechainicio': "⛔ Error: La fecha de inicio no puede ser futura."})
            if self.fechainicio < date(2005, 1, 1):
                raise ValidationError({'fechainicio': "⛔ Error: La fecha de inicio no puede ser anterior a 2005."})

        # Validar Fin
        if self.fechafin:
            if self.fechafin > date.today():
                raise ValidationError({'fechafin': "⛔ Error: La fecha de fin no puede ser futura."})
            if self.fechafin < date(2005, 1, 1):
                raise ValidationError({'fechafin': "⛔ Error: La fecha de fin no puede ser anterior a 2005."})

        # Validar Coherencia
        if self.fechafin and self.fechainicio and self.fechafin < self.fechainicio:
            raise ValidationError("⛔ Error Lógico: El curso no puede terminar antes de empezar.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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

    # --- VALIDACIÓN DE FECHA EN RECONOCIMIENTOS ---
    def clean(self):
        if self.fechareconocimiento:
            if self.fechareconocimiento > date.today():
                raise ValidationError({'fechareconocimiento': "⛔ Error: La fecha del reconocimiento no puede ser futura."})
            if self.fechareconocimiento < date(2005, 1, 1):
                raise ValidationError({'fechareconocimiento': "⛔ Error: La fecha no puede ser anterior a 2005."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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

    # --- VALIDACIÓN DE FECHA PRODUCTOS ---
    def clean(self):
        if self.fechaproducto:
            if self.fechaproducto > date.today():
                raise ValidationError({'fechaproducto': "⛔ Error: La fecha del producto no puede ser futura."})
            if self.fechaproducto < date(2005, 1, 1):
                raise ValidationError({'fechaproducto': "⛔ Error: La fecha no puede ser anterior a 2005."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# --- VENTA GARAGE ---
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

    # --- VALIDACIÓN DE PRECIO NEGATIVO ---
    def clean(self):
        if self.valordelbien is not None and self.valordelbien < 0:
            raise ValidationError({'valordelbien': "⛔ Error: ¡El precio no puede ser negativo! No puedes pagar para que se lo lleven."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)