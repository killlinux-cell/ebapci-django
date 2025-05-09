from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Classe, Membre, Presence

class CustomUserAdmin(UserAdmin):
    # Ajoute le champ "role" aux sections existantes
    fieldsets = UserAdmin.fieldsets + (
        ('Rôle utilisateur', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rôle utilisateur', {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']


admin.site.register(User, CustomUserAdmin)

class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'moniteur')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'moniteur':
            return qs.filter(moniteur=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'moniteur' and obj is not None:
            return obj.moniteur == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 'moniteur' and obj is not None:
            return obj.moniteur == request.user
        return True

admin.site.register(Classe, ClasseAdmin)

class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'classe')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'moniteur':
            return qs.filter(classe__moniteur=request.user)
        return qs

admin.site.register(Membre, MembreAdmin)


class PresenceAdmin(admin.ModelAdmin):
    list_display = ('membre', 'date', 'present')
    list_filter = ('date', 'present', 'membre__classe')
    search_fields = ('membre__nom',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'moniteur':
            return qs.filter(membre__classe__moniteur=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.role == 'moniteur' and obj is not None:
            return obj.membre.classe.moniteur == request.user
        return True

admin.site.register(Presence, PresenceAdmin)
