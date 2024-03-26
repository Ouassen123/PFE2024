from django.shortcuts import render, get_object_or_404, redirect
from .models import Livre, Auteur
from .forms import LivreForm, AuteurForm
from .scraper import scrape_data

def liste_livres(request):
    livres = Livre.objects.all()
    return render(request, 'liste_livres.html', {'livres': livres})

def ajouter_livre(request):
    if request.method == 'POST':
        form = LivreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        form = LivreForm()
    return render(request, 'ajouter_livre.html', {'form': form})

def modifier_livre(request, livre_id):
    livre = get_object_or_404(Livre, pk=livre_id)
    if request.method == 'POST':
        form = LivreForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        form = LivreForm(instance=livre)
    return render(request, 'modifier_livre.html', {'form': form})

def supprimer_livre(request, livre_id):
    livre = get_object_or_404(Livre, pk=livre_id)
    livre.delete()
    return redirect('liste_livres')

def ajouter_auteur(request):
    if request.method == 'POST':
        form = AuteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        auteur_id = request.GET.get('auteur_id')
        if auteur_id:
            auteur = get_object_or_404(Auteur, pk=auteur_id)
            form = AuteurForm(instance=auteur)
        else:
            form = AuteurForm()

    return render(request, 'ajouter_auteur.html', {'form': form})

def modifier_auteur(request, auteur_id):
    auteur = get_object_or_404(Auteur, pk=auteur_id)
    if request.method == 'POST':
        form = AuteurForm(request.POST, instance=auteur)
        if form.is_valid():
            form.save()
            return redirect('liste_livres')
    else:
        form = AuteurForm(instance=auteur)

    return render(request, 'modifier_auteur.html', {'form': form, 'auteur': auteur})

def supprimer_auteur(request, auteur_id):
    auteur = get_object_or_404(Auteur, pk=auteur_id)
    auteur.delete()
    return redirect('liste_livres')

def afficher_livres_scrapes(request):
    livres_scrapes = scrape_data()
    return render(request, 'afficher_livres_scrapes.html', {'livres_scrapes': livres_scrapes})
