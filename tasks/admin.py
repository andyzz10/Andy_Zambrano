from django.contrib import admin
from .models import Task, DatosPersonales, ExperienciaLaboral, Habilidad, Reconocimiento, Educacion, ProductoGarage, RecursoAcademico

# Mantenemos el registro de Task que ya tenías
admin.site.register(Task)

# Registramos los nuevos modelos para tu CV estilo Credentially
admin.site.register(DatosPersonales)
admin.site.register(ExperienciaLaboral)
admin.site.register(Habilidad)
admin.site.register(Reconocimiento)
admin.site.register(Educacion)
admin.site.register(ProductoGarage)
admin.site.register(RecursoAcademico)