from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
import pathlib


import subprocess
import sys
import os, logging
from datetime import datetime

from .models import Post, Image, Email, GalleryItem, Ceny
from .forms import PostForm, EmailForm, AddCenyForm 

from django.db import connection
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy
from .utils import get_price, detect_source_type, save_post_with_images, save_ceny_instance


from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Post, Image, Email, GalleryItem, Ceny 

from .serializers import PostSerializer, ImageSerializer, EmailSerializer, GalleryItemSerializer, CenySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet


class PostViewSet(ModelViewSet): 
    queryset = Post.objects.all() 
    serializer_class = PostSerializer 
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
class ImageViewSet(ModelViewSet): 
    queryset = Image.objects.all() 
    serializer_class = ImageSerializer 
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class EmailViewSet(CreateModelMixin, GenericViewSet): 
    queryset = Email.objects.all() 
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]
    
class GalleryItemViewSet(ReadOnlyModelViewSet): 
    queryset = GalleryItem.objects.all() 
    serializer_class = GalleryItemSerializer 
    permission_classes = [AllowAny]
    
class CenyViewSet(ReadOnlyModelViewSet): 
    queryset = Ceny.objects.all() 
    serializer_class = CenySerializer
    permission_classes = [AllowAny]

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # Získať zoznam obrázkov pre každý príspevok
    images_dict = {}
    for post in posts:
        images = Image.objects.filter(post=post)
        images_dict[post.pk] = images
    return render(request, 'zivotopis/post_list.html', {'posts': posts, 'images_dict': images_dict})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    images = Image.objects.filter(post=post)
    return render(request, 'zivotopis/post_detail.html', {'post': post, 'images': images})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'zivotopis/post_edit.html', {'form': form})



@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        image_files = request.FILES.getlist('images')
        if form.is_valid():
            post = save_post_with_images(form, request.user, image_files)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'zivotopis/post_edit.html', {'form': form, 'post': post})


@login_required
def image_delete(request, pk):
    image = get_object_or_404(Image, pk=pk)
    post_pk = image.post.pk
    if request.method == "POST":
        image.delete()
    return redirect('post_edit', pk=post_pk)


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'zivotopis/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk): 
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def success_view(request):
    return render(request, 'zivotopis/success.html')

def unsuccess_view(request):
    return render(request, 'zivotopis/unsuccess.html')

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            adresa = 'ruzbacky@yahoo.com'
            predmet = 'Nová zpráva z životopis formulára!'
            meno = 'Meno odosielateľa: ' + form.cleaned_data['sender_name']
            sprava = '\nSpráva: ' + form.cleaned_data['message'] 
            hlavicka = '\nJeho emailová adresa:\n' + form.cleaned_data['sender_email']
            hlavicka += "\nMIME-Version: 1.0\nContent-Type: text/html; charset=\"utf-8\"\n"
            predmet_odosielatela = 'Predmet: ' + form.cleaned_data['subject']

            send_mail(
                predmet,
                form.cleaned_data['subject'],
                form.cleaned_data['sender_email'],
                [adresa],
                fail_silently=False,
                html_message=meno + hlavicka + predmet_odosielatela + sprava
            )
            return redirect('success_view')
        else:
            # Pri nevalidnom formulári redirect na unsuccess_view
            return redirect('unsuccess_view')
    else:
        form = EmailForm()    
    return render(request, 'registration/send_email.html', {'form': form})

def zivo_view(request):
    icons_data = [
        ('house-door-fill.svg', 'Bratislava'),
        ('telephone-fill.svg', '+421 948 900 850'),
        ('envelope-fill.svg', 'ruzbacky@yahoo.com'),
        ('calendar-event-fill.svg', '48r.')
    ]
    return render(request, 'zivotopis/zivo.html', {'icons_data': icons_data})

def ang_zivo_view(request):
    icons_data = [
        ('house-door-fill.svg', 'Bratislava'),
        ('telephone-fill.svg', '+421 948 900 850'),
        ('envelope-fill.svg', 'ruzbacky@yahoo.com'),
        ('calendar-event-fill.svg', '48r.')
    ]
    return render(request, 'zivotopis/angzivo.html', {'icons_data': icons_data})

def gallery_view(request):
    items = GalleryItem.objects.all().order_by('-created')
    return render(request, 'zivotopis/gallery.html', {'items': items}) # Zobrazíme šablónu gallery.html

def home_view(request):
    source = request.GET.get('type', 'book')  # defaultne 'book'
    error = None
    form = AddCenyForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            instance, error = save_ceny_instance(form, get_price, detect_source_type)
            if instance:
                print(f"🔍 Pridávam {instance.source_type}: {instance.name} za {instance.now_price} €")
                return redirect(f"{reverse('home')}?type={instance.source_type}")
        else:
            error = form.errors

    items = Ceny.objects.filter(source_type=source)
    no_discounted = items.filter(differ_price__lt=0).count()

    context = {
        'quse': items,
        'items_no': items.count(),
        'no_discounted': no_discounted,
        'form': form,
        'error': error,
        'source_type': source,
    }

    return render(request, 'ceny/main.html', context)



class CenyDeleteView(LoginRequiredMixin, DeleteView):
    model = Ceny
    template_name = 'ceny/confirm_del.html'
    success_url = reverse_lazy('home')
    


def update_prices(request):
    source = request.GET.get('type', 'book')
    quse = Ceny.objects.filter(source_type=source)

    for link in quse:
        try:
            link.save()
        except Exception as e:
            print(f"❌ Chyba pri aktualizácii {link.url}: {e}")

    # Pridaj vizuálnu správu
    messages.success(request, "Ceny boli aktualizované ✅")

    # Presmeruj späť na home s aktuálnym typom
    return redirect(f"{reverse('home')}?type={source}")



def sql_test_view(request):
    query = ''
    result = None
    error = None

    # zoznam povolených cvičných tabuliek
    allowed_tables = ["sql_playground", "students", "courses", "teachers"]

    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        try:
            # kontrola – príkaz musí obsahovať aspoň jednu povolenú tabuľku
            if not any(tbl in query.lower() for tbl in allowed_tables):
                raise Exception(f"Povolené sú len príkazy nad tabuľkami: {', '.join(allowed_tables)}")

            with connection.cursor() as cursor:
                cursor.execute(query)
                if cursor.description:  # SELECT
                    result = cursor.fetchall()
                else:  # UPDATE/DELETE/INSERT
                    result = f"{cursor.rowcount} riadkov ovplyvnených"
        except Exception as e:
            error = str(e)

    return render(request, 'zivotopis/sql_test.html', {
        'query': query,
        'result': result,
        'error': error,
        'allowed_tables': allowed_tables,   # ➜ pridáme do kontextu
    })

def run_tests_page(request): 
    # zobrazí HTML stránku s tlačidlom a výstupom 
    return render(request, "zivotopis/test_page.html")

logger = logging.getLogger(__name__)

def extract_stats(stdout: str):
    lines = stdout.splitlines()
    passed = sum(1 for line in lines if "... ok" in line)
    failed = sum(1 for line in lines if "... FAIL" in line)
    errors = sum(1 for line in lines if "... ERROR" in line)
    total = passed + failed + errors
    return passed, failed, errors, total

def run_tests(request):
    try:
        is_remote = "PYTHONANYWHERE_DOMAIN" in os.environ
        

        if is_remote:
            python_bin = "/home/RastislavRuzbacky/.virtualenvs/rastislavruzbacky.eu.pythonanywhere.com/bin/python"
            project_root = "/home/RastislavRuzbacky/rastislavruzbacky.eu.pythonanywhere.com"
            
        else:
            python_bin = sys.executable
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            

        # 🦆 Spustíme testy cez coverage
        command = [
            python_bin,
            "-m", "coverage", "run",
            
            "-m", "django",
            "test",
            "--verbosity=2"
        ]


        env = os.environ.copy()
        env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")


        result = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env=env,
            timeout=120
        )

        success = result.returncode == 0
        combined_output = result.stdout + "\n" + result.stderr
        passed, failed, errors, total = extract_stats(combined_output)

        # 🦆 Spustíme coverage report
        coverage_command = [python_bin, "-m", "coverage", "report", "-m"]
        coverage_result = subprocess.run(
            coverage_command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env=env
        )
        coverage_output = coverage_result.stdout

        # 📁 Export výstupu do súboru
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"test_output_{timestamp}.txt"
        media_dir = os.path.join(project_root, "media")
        os.makedirs(media_dir, exist_ok=True)
        output_path = os.path.join(media_dir, filename)

        export_text = f"""
        📅 Dátum: {timestamp}
        📂 Modul: celý projekt
        ✅ Úspešné: {passed}
        ❌ Zlyhané: {failed}
        ⚠️ Chybné: {errors}
        📊 Počet testov: {total}

        --- Pokrytie kódu ---
        {coverage_output}

        --- Výstup testov ---
        {combined_output}
        """

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(export_text)

        return JsonResponse({
            "success": success,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "coverage": coverage_output,
            "download_url": f"/media/{filename}"
        })

    except Exception as e:
        logger.exception("❌ Chyba pri spúšťaní testov:")
        return JsonResponse({
            "success": False,
            "stdout": "",
            "stderr": str(e)
        })



# Create your views here.
