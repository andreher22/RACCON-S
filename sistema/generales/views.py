# ============================================================
# IMPORTS
# ============================================================
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import logout
from .models import Curso, Docente
import re

from django.urls import reverse
from .models import Reporte
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from datetime import datetime, timedelta

# ============================================================
# HOME
# ============================================================
class HomeView(TemplateView):
    template_name = "home.html"


# ============================================================
# USUARIOS DE PRUEBA (LOCALES)
# ============================================================
admins = {'admin1': '1234', 'admin2': '1234', 'admin3': '1234'}
docentes_fake = {'doc1': '1234', 'doc2': '1234', 'doc3': '1234'}
alumnos = {'alum1': '1234', 'alum2': '1234', 'alum3': '1234'}

registros_estudiantes = []


# ============================================================
# LOGIN ADMINISTRADOR
# ============================================================
def login_admin(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        if usuario in admins and admins[usuario] == password:
            request.session["rol"] = "administrador"
            request.session["usuario"] = usuario
            return render(request, "base.html", {"usuario": usuario, "rol": "administrador"})
        else:
            return render(request, "login/administrador.html", {"error": "Credenciales incorrectas"})

    return render(request, "login/administrador.html")


# ============================================================
# LOGIN DOCENTE
# ============================================================
def login_docente(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        if usuario in docentes_fake and docentes_fake[usuario] == password:
            request.session["rol"] = "docente"
            request.session["usuario"] = usuario
            return render(request, "base.html", {"usuario": usuario, "rol": "docente"})
        else:
            return render(request, "login/docente.html", {"error": "Credenciales incorrectas"})

    return render(request, "login/docente.html")


# ============================================================
# LOGIN ESTUDIANTE
# ============================================================
def login_estudiante(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        if usuario in alumnos and alumnos[usuario] == password:
            request.session["rol"] = "alumno"
            request.session["usuario"] = usuario
            return render(request, "base.html", {"usuario": usuario, "rol": "alumno"})
        else:
            return render(request, "login/estudiante.html", {"error": "Credenciales incorrectas"})

    return render(request, "login/estudiante.html")


# ============================================================
# REGISTRO ESTUDIANTE
# ============================================================
def registro_estudiante(request):
    if request.method == "POST":
        carrera = request.POST.get("carrera")
        cuatrimestre = request.POST.get("cuatrimestre")
        grupo = request.POST.get("grupo")
        matricula = request.POST.get("matricula")
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")
        confirmar = request.POST.get("confirmar_password")

        errores = []

        if not all([carrera, cuatrimestre, grupo, matricula, nombre, correo, usuario, password, confirmar]):
            errores.append("Todos los campos son obligatorios.")
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            errores.append("Correo electrónico inválido.")
        elif password != confirmar:
            errores.append("Las contraseñas no coinciden.")
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$', password):
            errores.append("La contraseña debe tener al menos 6 caracteres, incluyendo letras y números.")
        elif usuario in alumnos:
            errores.append("El usuario ya está registrado.")

        if errores:
            return render(request, "register/estudiante_r.html", {"errores": errores})

        nuevo_estudiante = {
            "carrera": carrera,
            "cuatrimestre": cuatrimestre,
            "grupo": grupo,
            "matricula": matricula,
            "nombre": nombre,
            "correo": correo,
            "usuario": usuario,
        }

        registros_estudiantes.append(nuevo_estudiante)
        alumnos[usuario] = password

        return render(request, "login/estudiante.html", {
            "mensaje": f"Registro exitoso. Bienvenido, {nombre}. Ahora puedes iniciar sesión."
        })

    return render(request, "register/estudiante_r.html")


# ============================================================
# CURSOS: LISTAR
# ============================================================
def cursos_view(request):
    rol = request.session.get("rol", "usuario")
    cursos = Curso.objects.all()

    return render(request, "menu/cursos.html", {
        "cursos": cursos,
        "rol": rol,
    })


# ============================================================
# CURSOS: CREAR
# ============================================================
def crear_curso_view(request):
    rol = request.session.get("rol", "usuario")

    if request.method == "POST":
        codigo = request.POST.get("codigo")
        nombre = request.POST.get("nombre")
        docente_id = request.POST.get("docente")

        docente = Docente.objects.get(id=docente_id)

        Curso.objects.create(
            codigo=codigo,
            nombre=nombre,
            docente=docente
        )

        # Redirige a la tabla de cursos
        return redirect("cursos")

    docentes = Docente.objects.all()

    return render(request, "menu/crear_curso.html", {
        "docentes": docentes,
        "rol": rol,
    })


# ============================================================
# CURSOS: VER DETALLE
# ============================================================
def ver_curso_view(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, "menu/ver_curso.html", {"curso": curso})


# ============================================================
# CURSOS: EDITAR
# ============================================================
def editar_curso_view(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    docentes = Docente.objects.all()
    rol = request.session.get("rol", "usuario")

    if request.method == "POST":
        curso.codigo = request.POST.get("codigo")
        curso.nombre = request.POST.get("nombre")
        docente_id = request.POST.get("docente")
        curso.docente = Docente.objects.get(id=docente_id)
        curso.save()

        return redirect("cursos")

    return render(request, "menu/editar_curso.html", {
        "curso": curso,
        "docentes": docentes,
        "rol": rol,
    })


# ============================================================
# LOGOUT
# ============================================================
def logout_view(request):
    logout(request)
    return redirect("home")


# ============================================================
# DOCENTES: LISTAR
# ============================================================
def docentes_view(request):
    docentes_list = Docente.objects.all()
    rol = request.session.get("rol", "usuario")

    return render(request, "menu/docentes.html", {
        "docentes_list": docentes_list,
        "rol": rol
    })


# ============================================================
# DOCENTES: CREAR REAL
# ============================================================
def crear_docente_view(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")

        Docente.objects.create(
            nombre=nombre,
            correo=correo,
        )

        # Redirige a la lista de docentes (tabla)
        return redirect("docentes")

    return render(request, "menu/crear_docente.html")


# ============================================================
# VISTA Generar Reporte PDF
# ============================================================
def generar_reporte_view(request):
    if request.method == "POST":
        
        # === Datos recibidos del formulario ===
        periodo = request.POST.get("periodo", "no-definido")
        tipo = request.POST.get("tipo", "reporte")

        # === Construcción del nombre del reporte ficticio ===
        fecha = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        titulo = f"Reporte {tipo.capitalize()} - {fecha}"

        # === URL ficticia para abrir ===
        url_falsa = "/media/reportes/reporte_demo.pdf"

        # === Guardar registro en DB ===
        Reporte.objects.create(
            titulo=titulo,
            periodo=periodo,
            url=url_falsa
        )

        return redirect("reportes")   # Redirecciona a la tabla

    return redirect("reportes")

# ============================================================
# VISTA PRICNIPAL Reportes
# ============================================================
def reportes_view(request):
    reportes = Reporte.objects.all().order_by("-creado")

    chart_report = {
        "labels": ['Curso A', 'Curso B', 'Curso C'],
        "data": [85, 78, 92]
    }

    return render(request, "menu/reportes.html", {
        "reportes": reportes,
        "chart_report": chart_report
    })


# ============================================================
# VISTA Actividades Recientes
# ============================================================
def dashboard(request):
    actividades = Actividad.objects.order_by('-fecha')[:3]
    return render(request, "menu/home.html", {
        "actividades": actividades
    })



# ============================================================
# VISTAS EVALUACIONES DOCENTE - ALUMNO
# ============================================================

# ===============================
# USUARIOS LOCALES FIJOS
# ===============================
DOCENTE_ACTUAL = "doc1"
ALUMNO_ACTUAL = "alum1"


# ===============================
# PREGUNTAS BASE
# ===============================
PREGUNTAS_BASE = [
    "El docente demuestra dominio de la materia.",
    "Explica los temas con claridad.",
    "Fomenta la participación en clase.",
    "Proporciona ejemplos útiles.",
    "Evalúa de forma justa y coherente.",
    "Responde dudas adecuadamente.",
    "Mantiene un ambiente de respeto.",
    "Utiliza materiales adecuados.",
    "Promueve el pensamiento crítico.",
    "Cumple con los tiempos y horarios establecidos."
]


# ===============================
# DOCENTE: VER EVALUACIONES
# ===============================
def evaluaciones(request):
    evaluaciones = Evaluacion.objects.filter(docente=DOCENTE_ACTUAL)

    return render(request, "menu/evaluaciones.html", {
        "rol": "docente",
        "evaluaciones": evaluaciones
    })


# ===============================
# DOCENTE: CREAR EVALUACIÓN
# ===============================
def crear_evaluacion(request):

    total = Evaluacion.objects.filter(docente=DOCENTE_ACTUAL).count() + 1

    evaluacion = Evaluacion.objects.create(
        titulo=f"Evaluación {total}",
        curso="Curso General",
        periodo="2025",
        docente=DOCENTE_ACTUAL
    )

    # Crear preguntas base
    for texto in PREGUNTAS_BASE:
        Pregunta.objects.create(evaluacion=evaluacion, texto=texto)

    # Asignar a alumno único
    EvaluacionPendiente.objects.create(
        alumno=ALUMNO_ACTUAL,
        evaluacion=evaluacion,
        vencimiento=datetime.now() + timedelta(days=7)
    )

    return redirect("evaluaciones")


# ===============================
# DOCENTE: VER UNA EVALUACIÓN
# ===============================
def ver_evaluacion(request, eval_id):
    evaluacion = Evaluacion.objects.get(id=eval_id)
    preguntas = Pregunta.objects.filter(evaluacion=evaluacion)

    return render(request, "menu/ver_evaluacion.html", {
        "evaluacion": evaluacion,
        "preguntas": preguntas
    })


# ===============================
# ALUMNO: VER PENDIENTES
# ===============================
def pendientes(request):

    pendientes = EvaluacionPendiente.objects.filter(alumno=ALUMNO_ACTUAL)

    return render(request, "menu/pendientes.html", {
        "pendientes": pendientes
    })


# ===============================
# ALUMNO: REALIZAR EVALUACIÓN
# ===============================
def realizar_evaluacion(request, pendiente_id):
    pendiente = EvaluacionPendiente.objects.get(id=pendiente_id)
    preguntas = Pregunta.objects.filter(evaluacion=pendiente.evaluacion)

    if request.method == "POST":
        total = 0

        for p in preguntas:
            valor = int(request.POST.get(f"preg_{p.id}"))
            total += valor
            Respuesta.objects.create(
                pendiente=pendiente,
                pregunta=p,
                valor=valor
            )

        puntaje = total / len(preguntas)

        Historial.objects.create(
            alumno=ALUMNO_ACTUAL,
            evaluacion=pendiente.evaluacion.titulo,
            curso=pendiente.evaluacion.curso,
            puntaje=puntaje
        )

        pendiente.delete()  # ya no aparece en pendientes

        return redirect("historial")

    return render(request, "menu/realizar_evaluacion.html", {
        "pendiente": pendiente,
        "preguntas": preguntas
    })


# ===============================
# HISTORIAL DE ALUMNO
# ===============================
def historial(request):
    datos = Historial.objects.filter(alumno=ALUMNO_ACTUAL)

    return render(request, "menu/historial.html", {
        "historial": datos
    })