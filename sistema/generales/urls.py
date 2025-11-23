from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    # Logins
    path("login/admin/", views.login_admin, name="login_admin"),
    path("login/docente/", views.login_docente, name="login_docente"),
    path("login/estudiante/", views.login_estudiante, name="login_estudiante"),

    # Registro estudiante
    path("registro/estudiante/", views.registro_estudiante, name="registro_estudiante"),
]

