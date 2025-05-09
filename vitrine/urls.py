from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('programmes/', views.programme_view, name='programme'),
    path('annonce/<int:pk>/', views.detail_annonce, name='detail_annonce'),
    path('contact/', views.contact_view, name='contact'),
    path('offrande/', views.offrande, name='offrande'),
    path('galerie/', views.galerie_list, name='galerie_list'),
    path('galerie/<int:galerie_id>/', views.galerie_detail, name='detail_galerie'),
    path('rencontres/', views.liste_rencontres, name='liste_rencontres'),
    path('rencontres/<int:pk>/', views.detail_rencontre, name='detail_rencontre'),
    path('rencontres/ajouter/', views.ajouter_rencontre, name='ajouter_rencontre'),
    path('rencontres/modifier/<int:pk>/', views.modifier_rencontre, name='modifier_rencontre'),
    path('rencontres/supprimer/<int:pk>/', views.supprimer_rencontre, name='supprimer_rencontre'),
    path('rencontres-gestion/', views.liste_rencontres_gestion, name='liste_rencontres_gestion'),

]
