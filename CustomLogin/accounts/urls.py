from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login_user/", views.login_user, name="login_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("login_admin/", views.login_admin, name="login_admin"),
    path("logout_admin/", views.logout_admin, name="logout_admin"),
    path("home_admin/", views.home_admin, name="home_admin"),
    path('userCreate/', views.user_create, name='user_create'),
    path('update/<int:id>/', views.update_user, name='update'),
    path('delete/<int:id>', views.delete_user, name='delete'),
    path("", views.home, name="home")
]
