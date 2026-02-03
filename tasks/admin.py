from django.contrib import admin
from .models import Task, DatosPersonales, ExperienciaLaboral, CursoRealizado, Reconocimiento, VentaGarage, ProductoAcademico, ProductoLaboral

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'nacionalidad')
    search_fields = ('nombres', 'apellidos', 'numerocedula')
    
    fieldsets = (
        ('Usuario y Foto', { 'fields': ('user', 'foto_portada', 'mostrar_botones') }),
        ('Configuración de Pestañas', { 
            'fields': ('mostrar_experiencia', 'mostrar_productos_laborales', 'mostrar_reconocimientos', 'mostrar_cursos', 'mostrar_productos_academicos', 'mostrar_garage')
        }),
        ('Información Básica', { 'fields': ('nombres', 'apellidos', 'descripcionperfil', 'nacionalidad', 'fechanacimiento', 'sexo') }),
        ('Datos Civiles', { 'fields': ('numerocedula', 'estadocivil', 'licenciaconducir') }),
        ('Contacto', { 'fields': ('telefonofijo', 'telefonoconvencional', 'direcciondomiciliaria', 'direcciontrabajo', 'sitioweb') }),
    )

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    list_filter = ('activarparaqueseveaenfront', 'nombrempresa')
    fieldsets = (
        ('Datos del Cargo', { 'fields': ('perfil', 'cargodesempenado', 'descripcionfunciones', 'activarparaqueseveaenfront') }),
        ('Empresa', { 'fields': ('nombrempresa', 'lugarempresa', 'emailempresa', 'sitiowebempresa') }),
        ('Contacto Referencia', { 'fields': ('nombrecontactoempresarial', 'telefonocontactoempresarial') }),
        ('Periodo', { 'fields': ('fechainiciogestion', 'fechafingestion', 'rutacertificado') }),
    )

@admin.register(CursoRealizado)
class CursoRealizadoAdmin(admin.ModelAdmin):
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'totalhoras', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    list_filter = ('activarparaqueseveaenfront', 'entidadpatrocinadora')
    fieldsets = (
        ('Detalles del Curso', { 'fields': ('perfil', 'nombrecurso', 'descripcioncurso', 'entidadpatrocinadora', 'activarparaqueseveaenfront') }),
        ('Duración', { 'fields': ('fechainicio', 'fechafin', 'totalhoras') }),
        ('Contacto y Certificado', { 'fields': ('nombrecontactoauspicia', 'telefonocontactoauspicia', 'emailempresapatrocinadora', 'rutacertificado') }),
    )

@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('descripcionreconocimiento', 'entidadpatrocinadora', 'tiporeconocimiento', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    list_filter = ('tiporeconocimiento', 'activarparaqueseveaenfront')
    fieldsets = (
        ('Detalles', { 'fields': ('perfil', 'descripcionreconocimiento', 'tiporeconocimiento', 'entidadpatrocinadora', 'fechareconocimiento') }),
        ('Contacto', { 'fields': ('nombrecontactoauspicia', 'telefonocontactoauspicia', 'rutacertificado', 'activarparaqueseveaenfront') }),
    )

@admin.register(ProductoAcademico)
class ProductoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    list_filter = ('activarparaqueseveaenfront', 'clasificador')
    fieldsets = (
        ('Información del Producto', { 'fields': ('perfil', 'nombrerecurso', 'clasificador', 'descripcion', 'activarparaqueseveaenfront') }),
    )

@admin.register(ProductoLaboral)
class ProductoLaboralAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    list_filter = ('activarparaqueseveaenfront',)
    fieldsets = (
        ('Información Laboral', { 'fields': ('perfil', 'nombreproducto', 'descripcion', 'fechaproducto', 'activarparaqueseveaenfront') }),
    )

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront')
    list_editable = ('activarparaqueseveaenfront',)
    list_filter = ('estadoproducto', 'activarparaqueseveaenfront')
    fieldsets = (
        ('Datos del Bien', { 'fields': ('perfil', 'nombreproducto', 'descripcion', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront') }),
        ('Multimedia', { 'fields': ('imagen',) }),
    )

admin.site.register(Task)