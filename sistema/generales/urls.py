# generales/urls.py
from django.urls import path
from . import views

urlpatterns = [

    # ============================================================
    # HOME
    # ============================================================
    path("", views.HomeView.as_view(), name="home"),

    # ============================================================
    # AUTENTICACIÓN
    # ============================================================
    # Logins
    path("login/admin/", views.login_admin, name="login_admin"),
    path("login/docente/", views.login_docente, name="login_docente"),
    path("login/estudiante/", views.login_estudiante, name="login_estudiante"),

    # Logout
    path("logout/", views.logout_view, name="logout"),

    # Registro estudiante
    path("registro/estudiante/", views.registro_estudiante, name="registro_estudiante"),

    # ============================================================
    # CURSOS
    # ============================================================
    path("cursos/", views.cursos_view, name="cursos"),
    path("cursos/crear/", views.crear_curso_view, name="crear_curso"),
    path("cursos/<int:curso_id>/", views.ver_curso_view, name="ver_curso"),
    path("cursos/<int:curso_id>/editar/", views.editar_curso_view, name="editar_curso"),

    # ============================================================
    # DOCENTES
    # ============================================================
    path("docentes/", views.docentes_view, name="docentes"),
    path("docentes/crear/", views.crear_docente_view, name="crear_docente"),

    # ============================================================
    # REPORTES
    # ============================================================
    path("reportes/", views.reportes_view, name="reportes"),
    path("reportes/generar/", views.generar_reporte_view, name="generar_reporte"),


    # ============================================================
    # EVALUACIONES DOCENTE - ALUMNO
    # ============================================================

    path("evaluaciones/", views.evaluaciones, name="evaluaciones"),
    path("crear-evaluacion/", views.crear_evaluacion, name="crear_evaluacion"),
    path("evaluacion/<int:eval_id>/", views.ver_evaluacion, name="ver_evaluacion"),

    path("pendientes/", views.pendientes, name="pendientes"),
    path("realizar/<int:pendiente_id>/", views.realizar_evaluacion, name="realizar_evaluacion"),

    path("historial/", views.historial, name="historial"),

]
