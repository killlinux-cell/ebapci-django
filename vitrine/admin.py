from django.contrib import admin
from .models import MessageContact, MediaGallery, Slide, Annonce, Programme, ImageGalerie, Galerie, RencontreQuotidienne


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre')
    ordering = ['ordre']

@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_published')
    list_filter = ('category',)
    search_fields = ('title', 'content')


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date')
    search_fields = ('nom', 'date')
    list_filter = ('date',)

class ImageGalerieInline(admin.TabularInline):
    model = ImageGalerie
    extra = 3  # nombre d’images à ajouter par défaut

@admin.register(Galerie)
class GalerieAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_ajout')
    inlines = [ImageGalerieInline]

admin.site.register(MessageContact)

@admin.register(RencontreQuotidienne)
class RencontreQuotidienneAdmin(admin.ModelAdmin):
    list_display = ('theme', 'date')
    search_fields = ('theme', 'text_biblique', 'message')
    list_filter = ('date',)
