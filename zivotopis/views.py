from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import subprocess
import sys
import socket
import os, logging


from .models import Post, Image, Email, GalleryItem, Ceny
from .forms import PostForm, ImageForm, EmailForm, AddCenyForm 

from django.db import connection
import requests
from bs4 import BeautifulSoup
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy
from .utils import get_price, detect_source_type, save_post_with_images, save_ceny_instance





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



class CenyDeleteView(DeleteView):
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


@login_required
def sql_test_view(request):
    query = ''
    result = None
    error = None

    if request.method == 'POST':
        query = request.POST.get('query', '')
        try:
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
        'error': error
    })    

def run_tests_page(request):
    return render(request, "zivotopis/test_page.html")

logger = logging.getLogger(__name__)

def run_tests(request):
    """Spustí testy: lokálne všetky, na PythonAnywhere len bezpečné."""
    try:
        # Zistenie, či bežíme na PythonAnywhere
        is_remote = "PYTHONANYWHERE_DOMAIN" in os.environ

        if is_remote:
            # 🟢 Remote – bezpečné testy cez Django modul
            test_path = "zivotopis/tests/test_save.py"
            python_bin = "/home/RastislavRuzbacky/.virtualenvs/rastislavruzbacky.eu.pythonanywhere.com/bin/python"
            project_root = "/home/RastislavRuzbacky/rastislavruzbacky.eu.pythonanywhere.com"
            settings_module = "mysite.settings_test"

            command = [
                python_bin,
                os.path.join(project_root, "manage.py"),
                "test",
                test_path,
                "--settings=" + settings_module,
                "--keepdb"
            ]
        else:
            # 💻 Lokálne – všetky testy cez manage.py
            test_path = "zivotopis"
            python_bin = sys.executable
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            settings_module = "mysite.settings"

            command = [
                python_bin,
                os.path.join(project_root, "manage.py"),
                "test",
                test_path,
                "--settings=" + settings_module
            ]

        env = os.environ.copy()
        env["DJANGO_SETTINGS_MODULE"] = settings_module
        env["PYTHONPATH"] = project_root

        logger.info(f"🧭 CWD: {project_root}")
        logger.info(f"🗂 manage.py exists: {os.path.exists(os.path.join(project_root, 'manage.py'))}")
        logger.info(f"💻 Command: {' '.join(command)}")

        result = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env=env,
            timeout=120
        )

        success = result.returncode == 0
        logger.info(f"✅ Return code: {result.returncode}")
        if result.stdout:
            logger.info(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            logger.error(f"STDERR:\n{result.stderr}")

        return JsonResponse({
            "success": success,
            "stdout": result.stdout,
            "stderr": result.stderr
        })

    except Exception as e:
        logger.exception("❌ Chyba pri spúšťaní testov:")
        return JsonResponse({
            "success": False,
            "stdout": "",
            "stderr": str(e)
        })


# Create your views here.
