from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import custom_logout_view

urlpatterns = [
    path('login/', views.connexion_view, name='login'),
    #path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard-moniteur/', views.dashboard_moniteur, name='dashboard_moniteur'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('presence/', views.pointer_presence, name='pointer_presence'),
    path('absences/', views.liste_absences, name='liste_absences'),
    path('redirect/', views.redirection_apres_login, name='redirect'),
    path('logout/', custom_logout_view, name='logout'),
    path('recapitulatif/', views.recapitulatif_presences, name='recapitulatif_presences'),

    path('ajouter-membre/', views.ajouter_membre, name='ajouter_membre'),
    path('supprimer-membre/<int:membre_id>/', views.supprimer_membre, name='supprimer_membre'),

    ]