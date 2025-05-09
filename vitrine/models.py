from django.db import models


CATEGORIES = (
    ('evenement', 'Événement'),
    ('communique', 'Communiqué'),
    ('annonce', 'Annonce'),
)

class Annonce(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_published = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    fichier = models.FileField(upload_to='annonces/', blank=True, null=True)

    def __str__(self):
        return self.title
class MessageContact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoye = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.sujet}"

class MediaGallery(models.Model):
    titre = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class Slide(models.Model):
    titre = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='slides/')
    actif = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)

    def __str__(self):
        return self.titre or f"Slide {self.id}"


class Programme(models.Model):
    nom = models.CharField(max_length=100)
    image = models.ImageField(upload_to='programmes/')
    date = models.CharField(max_length=100)  # ou models.DateTimeField si besoin
    description = models.TextField()

    def __str__(self):
        return self.nom


class Galerie(models.Model):
    titre = models.CharField(max_length=200)
    couverture = models.ImageField(upload_to='galeries/couvertures/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class ImageGalerie(models.Model):
    galerie = models.ForeignKey(Galerie, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='galeries/images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image pour {self.galerie.titre}"



class RencontreQuotidienne(models.Model):
    theme = models.CharField(max_length=255)
    date = models.DateField()
    text_biblique = models.TextField()
    message = models.TextField()
    apercu = models.TextField()
    application = models.TextField()
    prieres = models.TextField()
    lecture_biblique_annuelle = models.TextField()

    class Meta:
        ordering = ['-date']  # Les plus récentes en premier
        verbose_name = "Rencontre quotidienne"
        verbose_name_plural = "Rencontres quotidiennes"

    def __str__(self):
        return f"{self.theme} - {self.date.strftime('%d/%m/%Y')}"



