from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactForm, RencontreForm
from .models import MediaGallery, Slide, Annonce, Programme, Galerie, RencontreQuotidienne


def accueil(request):
    slides = Slide.objects.order_by('ordre')
    annonces = Annonce.objects.order_by('-date_published')[:3]
    return render(request, 'vitrine/accueil.html', {'slides': slides, 'annonces': annonces})
def horaires(request):
    return render(request, 'vitrine/horaires.html')

#def galerie(request):
#    return render(request, 'vitrine/galerie.html')

def annonces(request):
    return render(request, 'vitrine/annonces.html')


def detail_annonce(request, pk):
    annonce = get_object_or_404(Annonce, pk=pk)
    fichier_url = annonce.fichier.url if annonce.fichier else ""
    extension = fichier_url.split('.')[-1].lower() if fichier_url else ""
    return render(request, 'vitrine/detail_annonce.html', {
        'annonce': annonce,
        'extension': extension,
    })

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a été envoyé avec succès.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'vitrine/contact.html', {'form': form})


def offrande(request):
    return render(request, 'vitrine/offrande.html')

def galerie_list(request):
    galeries = Galerie.objects.all().order_by('-date_ajout')
    return render(request, 'vitrine/galerie_list.html', {'galeries': galeries})

def galerie_detail(request, galerie_id):
    galerie = get_object_or_404(Galerie, pk=galerie_id)
    return render(request, 'vitrine/galerie_detail.html', {'galerie': galerie})
def programme_view(request):
    programmes = Programme.objects.all()
    return render(request, 'vitrine/programme.html', {'programmes': programmes})


def liste_rencontres(request):
    rencontres = RencontreQuotidienne.objects.all()
    return render(request, 'vitrine/rencontre.html', {'rencontres': rencontres})


def detail_rencontre(request, pk):
    rencontre = get_object_or_404(RencontreQuotidienne, pk=pk)
    return render(request, 'vitrine/rencontre_detail.html', {'rencontre': rencontre})



def ajouter_rencontre(request):
    if request.method == 'POST':
        form = RencontreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_rencontres')
    else:
        form = RencontreForm()
    return render(request, 'vitrine/rencontres/form.html', {'form': form, 'title': 'Ajouter une Rencontre'})

def modifier_rencontre(request, pk):
    rencontre = get_object_or_404(RencontreQuotidienne, pk=pk)
    form = RencontreForm(request.POST or None, instance=rencontre)
    if form.is_valid():
        form.save()
        return redirect('liste_rencontres')
    return render(request, 'vitrine/rencontres/form.html', {'form': form, 'title': 'Modifier la Rencontre'})

def supprimer_rencontre(request, pk):
    rencontre = get_object_or_404(RencontreQuotidienne, pk=pk)
    if request.method == 'POST':
        rencontre.delete()
        return redirect('liste_rencontres')
    return render(request, 'vitrine/rencontres/supprimer.html', {'rencontre': rencontre})


def est_responsable(user):
    return user.is_authenticated and user.groups.filter(name="Responsables Rencontres").exists()
@user_passes_test(est_responsable)
def liste_rencontres_gestion(request):
    rencontres = RencontreQuotidienne.objects.all().order_by('-date')
    return render(request, 'vitrine/rencontres/liste.html', {'rencontres': rencontres})


@login_required
def redirection_apres_login(request):
    user = request.user
    if user.groups.filter(name="Responsables Rencontres").exists():
        return redirect('liste_rencontres_gestion')  # nom de l’URL vers liste.html
    else:
        return redirect('accueil')  # ou une autre page par défaut