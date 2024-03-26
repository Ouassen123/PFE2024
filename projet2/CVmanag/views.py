from django.shortcuts import get_object_or_404, render, redirect
from .models import CV, JobOffer, UserProfile, Job
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import spacy
import fitz
import os
from django.contrib.auth.decorators import login_required
from .forms import JobOfferForm

nlp = spacy.load('fr_core_news_sm')

@login_required
def process_cv(request):
    if request.method == 'POST':
        cv_file = request.FILES['cv_file']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        experience_years = int(request.POST['experience'])
        requirements = request.POST['requirements']

        media_dir = os.path.join('media', 'uploads')
        os.makedirs(media_dir, exist_ok=True)

        # save le fichier pdf dans media/uplods
        cv_file_path = os.path.join(media_dir, cv_file.name.replace(" ", "_"))
        with open(cv_file_path, 'wb') as destination:
            for chunk in cv_file.chunks():
                destination.write(chunk)

        # extraire le texte du PDF moi jai utiliser PyMuPDF
        def extract_text_from_pdf(pdf_file):
            doc = fitz.open(pdf_file)
            text = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            return text

        cv_text = extract_text_from_pdf(cv_file_path)
        cleaned_text = ' '.join([token.lemma_ for token in nlp(cv_text) if not token.is_stop and token.is_alpha])

        # Enregistrer le CV dans la base de données
        new_cv = CV.objects.create(
            user=request.user,
            file=cv_file_path,
            text_content=cleaned_text,
            first_name=first_name,
            last_name=last_name,
            experience_years=experience_years
        )
        # TF-IDF
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform([cleaned_text])
        requirements_vector = tfidf_vectorizer.transform([requirements])

        # les mot similar
        cosine_similarity = linear_kernel(requirements_vector, tfidf_matrix).flatten()

        # Renvoyer le résultat à la template
        return render(request, 'result.html', {'cv_path': new_cv.file.url, 'cosine_similarity': cosine_similarity[0]})

    return render(request, 'upload_cv.html')

@login_required
def job_offers(request):
    offers = JobOffer.objects.all()
    return render(request, 'job_offers.html', {'offers': offers})

@login_required
def apply_job(request, offer_id):
    offer = get_object_or_404(JobOffer, pk=offer_id)
    if request.method == 'POST':
        # Logique de postulation ici
        return redirect('job_offers')
    return render(request, 'apply_job.html', {'offer': offer})
def home(request):
    offers = JobOffer.objects.all()
    return render(request, 'home.html', {'offers': offers})
@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile})
@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            job_offer = form.save(commit=False)
            job_offer.recruiter = request.user
            job_offer.save()
    else:
        form = JobOfferForm()

    return render(request, 'profile.html', {'user_profile': user_profile, 'form': form})
def job_info(request, offer_id):
    offer = get_object_or_404(JobOffer, pk=offer_id)
    return render(request, 'job_info.html', {'offer': offer})
def create_job_offer(request):
    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            job_offer = form.save(commit=False)
            job_offer.recruiter = request.user
            job_offer.save()
            
            # Récupérer les données du formulaire
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            required_experience = form.cleaned_data['required_experience']
            
            # Créer un nouvel emploi associé à l'offre d'emploi
            job = Job.objects.create(
                title=title,
                salary=form.cleaned_data['salary'],
                details=form.cleaned_data['details'],
                image=form.cleaned_data['image']
            )
            
            # Associer l'emploi à l'offre d'emploi créée
            job_offer.job = job
            job_offer.save()
            
            return redirect('job_offers')  # Rediriger vers une page appropriée après la création de l'offre d'emploi
    else:
        form = JobOfferForm()
        
    return render(request, 'create_job_offer.html', {'form': form})
