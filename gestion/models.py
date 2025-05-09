from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.shortcuts import redirect, render


# Utilisateur personnalisé
class User(AbstractUser):
    ROLE_CHOICES = (
        ('moniteur', 'Moniteur'),
        ('gest_rencontre', 'Gestion Rencontre'),
        ('admin', 'Super Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_moniteur(self):
        return self.role == 'moniteur'

    def is_admin(self):
        return self.role == 'admin'

    def is_gest_rencontre(self):
        return self.role == 'gest_rencontre'

# Classe
class Classe(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    moniteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='classes')

    def __str__(self):
        return self.nom

# Membre
class Membre(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    age = models.IntegerField()
    telephone = models.CharField(max_length=20)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# Présence
class Presence(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('membre', 'date')

    def __str__(self):
        return f"{self.membre} - {self.date} - {'Présent' if self.present else 'Absent'}"


