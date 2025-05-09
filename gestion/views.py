from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now
from django.views.decorators.cache import never_cache

from . import forms
from .forms import MembreForm
from .models import User, Membre, Presence, Classe
from datetime import date


def connexion_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Rediriger selon le rôle
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'moniteur':
                return redirect('dashboard_moniteur')
            elif user.role == 'gest_rencontre':
                return redirect('liste_rencontres_gestion')
        else:
            return render(request, 'gestion/login.html', {'error': 'Identifiants invalides'})

    return render(request, 'gestion/login.html')

#@login_required
#def dashboard_admin(request):
#    if request.user.role != 'admin':
#        return redirect('unauthorized')
#    return render(request, 'gestion/dashboard_admin.html')

@login_required
def dashboard_moniteur(request):
    if request.user.role != 'moniteur':
        return redirect('unauthorized')
    return render(request, 'gestion/dashboard_moniteur.html')

def unauthorized(request):
    return render(request, 'gestion/unauthorized.html')


@login_required
def pointer_presence(request):
    # Obtenir les classes assignées au moniteur connecté
    classes_moniteur = Classe.objects.filter(moniteur=request.user)

    # Filtrer les membres uniquement dans ces classes
    membres = Membre.objects.filter(classe__in=classes_moniteur)

    today = now().date()

    if request.method == 'POST':
        for membre in membres:
            present = request.POST.get(f'present_{membre.id}') == 'on'
            # Créer la présence uniquement si elle n'existe pas
            Presence.objects.get_or_create(
                membre=membre,
                date=today,
                defaults={'present': present}
            )
        return redirect('dashboard_moniteur')  # Rediriger pour éviter les doublons sur refresh

    return render(request, 'gestion/pointer_presence.html', {'membres': membres, 'date': today})


@login_required
def liste_absences(request):
    selected_date = request.GET.get('date')
    presences = []

    if selected_date:
        presences = Presence.objects.filter(date=selected_date)

    return render(request, 'gestion/liste_absences.html', {
        'presences': presences,
        'selected_date': selected_date,
    })


@login_required
def redirection_apres_login(request):
    user = request.user

    if user.role == 'superadmin':
        return redirect('/admin/')  # Tableau de bord admin Django
    elif user.role == 'moniteur':
        return redirect('dashboard_moniteur')  # Ton tableau de bord spécifique
    elif user.role == 'gest_rencontre':
        return redirect('/rencontres-gestion/')
    else:
        return redirect('/')  # Vers le site vitrine public par exemple


@never_cache
@login_required
def dashboard_moniteur(request):
    user = request.user
    classes = Classe.objects.filter(moniteur=user)

    classes_data = []
    for classe in classes:
        membres = Membre.objects.filter(classe=classe)
        classes_data.append({
            'classe': classe,
            'membres': membres,
        })

    return render(request, 'gestion/dashboard_moniteur.html', {
        'classes_data': classes_data
    })


@login_required
def ajouter_membre(request):
    user = request.user
    classe = Classe.objects.filter(moniteur=user).first()

    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            membre = form.save(commit=False)
            membre.classe = classe
            membre.save()
            return redirect('dashboard_moniteur')
    else:
        form = MembreForm()

    return render(request, 'gestion/ajouter_membre.html', {'form': form})


@login_required
def supprimer_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)

    if request.method == 'POST':
        membre.delete()
        return redirect('dashboard_moniteur')


def custom_logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')


@login_required
def recapitulatif_presences(request):
    # Récupérer les classes du moniteur connecté
    classes_moniteur = Classe.objects.filter(moniteur=request.user)

    # Récupérer les membres de ces classes uniquement
    membres = Membre.objects.filter(classe__in=classes_moniteur)

    data = []

    for membre in membres:
        total_jours = Presence.objects.filter(membre=membre).count()
        jours_presents = Presence.objects.filter(membre=membre, present=True).count()
        jours_absents = Presence.objects.filter(membre=membre, present=False).count()

        taux_presence = (jours_presents / total_jours * 100) if total_jours else 0

        data.append({
            'membre': membre,
            'jours_presents': jours_presents,
            'jours_absents': jours_absents,
            'taux_presence': round(taux_presence, 2),
        })

    return render(request, 'gestion/recapitulatif_presences.html', {'data': data})


from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import Classe, Membre
from .forms import CreateMoniteurForm, AssignMoniteurForm

User = get_user_model()

@login_required
def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.role == 'admin':
        return redirect('login')

    classes = Classe.objects.all()
    create_moniteur_form = CreateMoniteurForm()
    assign_moniteur_form = AssignMoniteurForm()

    if request.method == 'POST':
        if 'create_moniteur' in request.POST:
            create_moniteur_form = CreateMoniteurForm(request.POST)
            if create_moniteur_form.is_valid():
                user = create_moniteur_form.save(commit=False)
                user.role = 'moniteur'
                user.set_password(create_moniteur_form.cleaned_data['password'])
                user.save()
                return redirect('admin_dashboard')

        elif 'assign_moniteur' in request.POST:
            assign_moniteur_form = AssignMoniteurForm(request.POST)
            if assign_moniteur_form.is_valid():
                classe = assign_moniteur_form.cleaned_data['classe']
                moniteur = assign_moniteur_form.cleaned_data['moniteur']
                classe.moniteur = moniteur
                classe.save()
                return redirect('admin_dashboard')

        elif 'remove_moniteur' in request.POST:
            classe_id = request.POST.get('classe_id')
            classe = Classe.objects.get(id=classe_id)
            classe.moniteur = None
            classe.save()
            return redirect('admin_dashboard')

    context = {
        'classes': classes,
        'create_moniteur_form': create_moniteur_form,
        'assign_moniteur_form': assign_moniteur_form,
    }
    return render(request, 'gestion/dashboard-admin.html', context)
