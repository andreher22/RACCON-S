# generales/models.py
from django.db import models

class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(default="correo@default.com")

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Reporte(models.Model):
    titulo = models.CharField(max_length=200)
    periodo = models.CharField(max_length=50)
    url = models.CharField(max_length=300)  # O FileField si luego generas PDF real
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


""" 
Modelo para registrar actividades del sistema, en Deshboard,
aunque no se logro una correcta implementación para que registre
las actividades en la vista del dashboard.

class Actividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.descripcion}"
"""

class Evaluacion(models.Model):
    titulo = models.CharField(max_length=200)
    curso = models.CharField(max_length=200)
    periodo = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, default="pendiente")
    docente = models.CharField(max_length=50)  # ahora texto: "doc1"
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Pregunta(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    texto = models.TextField()


class EvaluacionPendiente(models.Model):
    alumno = models.CharField(max_length=50)  # ahora texto: "alum1"
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    vencimiento = models.DateField()


class Respuesta(models.Model):
    pendiente = models.ForeignKey(EvaluacionPendiente, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    valor = models.IntegerField()  # 1 a 5



class Historial(models.Model):
    alumno = models.CharField(max_length=50)
    evaluacion = models.CharField(max_length=200)
    curso = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    puntaje = models.FloatField()