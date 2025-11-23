from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import re  # Import necesario para validaciones con expresiones regulares

# Página principal
class HomeView(TemplateView):
    template_name = "home.html"


# Usuarios de ejemplo (locales)
admins = {'admin1': '1234', 'admin2': '1234', 'admin3': '1234'}
docentes = {'doc1': '1234', 'doc2': '1234', 'doc3': '1234'}
alumnos = {'alum1': '1234', 'alum2': '1234', 'alum3': '1234'}

# Simulación de base de datos de registros (solo para pruebas)
registros_estudiantes = []


# ---------- ADMINISTRADOR ----------
def login_admin(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        if usuario in admins and admins[usuario] == password:
            return render(request, "base.html", {"usuario": usuario, "rol": "administrador"})
        else:
            return render(request, "login/administrador.html", {"error": "Credenciales incorrectas"})

    return render(request, "login/administrador.html")




# ---------- DOCENTE ----------
def login_docente(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        if usuario in docentes and docentes[usuario] == password:
            return render(request, "base.html", {"usuario": usuario, "rol": "docente"})
        else:
            return render(request, "login/docente.html", {"error": "Credenciales incorrectas"})

    return render(request, "login/docente.html")


# ---------- ESTUDIANTE ----------
def login_estudiante(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        if usuario in alumnos and alumnos[usuario] == password:
            return render(request, "base.html", {"usuario": usuario, "rol": "alumno"})
        else:
            return render(request, "login/estudiante.html", {"error": "Credenciales incorrectas"})

    return render(request, "login/estudiante.html")


# ---------- REGISTRO ESTUDIANTE ----------
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

        # ----- VALIDACIONES -----
        errores = []

        # Validar campos vacíos
        if not all([carrera, cuatrimestre, grupo, matricula, nombre, correo, usuario, password, confirmar]):
            errores.append("Todos los campos son obligatorios.")

        # Validar correo
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            errores.append("Correo electrónico inválido.")

        # Validar contraseñas iguales
        elif password != confirmar:
            errores.append("Las contraseñas no coinciden.")

        # Validar contraseña segura
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$', password):
            errores.append("La contraseña debe tener al menos 6 caracteres, incluyendo letras y números.")

        # Validar usuario duplicado
        elif usuario in alumnos:
            errores.append("El usuario ya está registrado.")

        # Si hay errores, volver con mensajes
        if errores:
            return render(request, "register/estudiante_r.html", {"errores": errores})
        
        # Validar usuario duplicado
        #if usuario in alumnos:
           # errores.append("El usuario ya está registrado.")
        # Validar matrícula duplicada
        #elif any(est["matricula"] == matricula for est in registros_estudiantes):
            #errores.append("La matrícula ya está registrada.")
        # Validar correo duplicado
        #elif any(est["correo"] == correo for est in registros_estudiantes):
            #errores.append("El correo ya está registrado.")


        # ---------- SIMULACIÓN DE REGISTRO ----------
        # Guardamos el nuevo estudiante en la lista y el diccionario
        nuevo_estudiante = {
            "carrera": carrera,
            "cuatrimestre": cuatrimestre,
            "grupo": grupo,
            "matricula": matricula,
            "nombre": nombre,
            "correo": correo,
            "usuario": usuario
        }
        registros_estudiantes.append(nuevo_estudiante)
        alumnos[usuario] = password  # Permite login luego

        # Redirige al login con mensaje
        return render(request, "login/estudiante.html", {
            "mensaje": f"Registro exitoso. Bienvenido, {nombre}. Ahora puedes iniciar sesión."
        })

    # Si solo abre la página de registro
    return render(request, "register/estudiante_r.html")

