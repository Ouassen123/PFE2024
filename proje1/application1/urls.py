from django.urls import path
from .views import liste_livres, ajouter_livre, modifier_livre, supprimer_livre, ajouter_auteur, modifier_auteur, supprimer_auteur,afficher_livres_scrapes 

urlpatterns = [
    path('livres/', liste_livres, name='liste_livres'),
    path('livres/ajouter/', ajouter_livre, name='ajouter_livre'),
    path('livres/modifier/<int:livre_id>/', modifier_livre, name='modifier_livre'),
    path('livres/supprimer/<int:livre_id>/', supprimer_livre, name='supprimer_livre'),
    path('auteurs/ajouter/', ajouter_auteur, name='ajouter_auteur'),
    path('auteurs/modifier/<int:auteur_id>/', modifier_auteur, name='modifier_auteur'),
    path('auteurs/supprimer/<int:auteur_id>/', supprimer_auteur, name='supprimer_auteur'),
    path('livres/scrapes/', afficher_livres_scrapes, name='afficher_livres_scrapes'),
]
