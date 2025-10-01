from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from .models import Post, Image, Email, GalleryItem, Ceny
from .forms import PostForm, ImageForm, EmailForm, AddCenyForm 

import requests
from bs4 import BeautifulSoup
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .utils import get_reality_price





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
        form = PostForm(request.POST, request.FILES)
        image_files = request.FILES.getlist('images')  # získaj všetky nahraté obrázky

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # vytvor Image objekty pre každý nahratý súbor
            for image_file in image_files:
                Image.objects.create(post=post, image=image_file)

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
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            for image_file in image_files:
                Image.objects.create(post=post, image=image_file)
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
            #hlavicka = format_html(
                #"<p>{}</p><p>MIME-Version: 1.0</p><p>Content-Type: text/html; charset=\"utf-8\"</p>",
                #meno + "<br>" + predmet_odosielatela + "<br>" + sprava
            #)    
            uspech = send_mail (predmet, 
                               form.cleaned_data['subject'], 
                               form.cleaned_data['sender_email'], 
                               [adresa], 
                               fail_silently=False, 
                               html_message=meno + hlavicka + predmet_odosielatela + sprava
                               )
            if uspech:
                return redirect('success_view')
        else:
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
    no_discounted = 0
    error = None
    
    form = AddCenyForm(request.POST or None)
    
    if request.method == 'POST':
        form = AddCenyForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            if instance.url:
                name, price = get_reality_price(instance.url)

                if name is None or price is None:
                    error = "Nepodarilo sa získať názov alebo cenu"
                else:
                    instance.name = name
                    instance.now_price = price
                    instance.old_price = price  # prvýkrát rovnaká
                    instance.differ_price = 0
                    instance.save()
                    return redirect('home')
            else:
                error = "URL je prázdna"
    else:
        error = form.errors

    
    quse = Ceny.objects.all()
    items_no = quse.count()
    
    if items_no > 0:
        discount_list = []
        for item in quse:
            if item.old_price > item.now_price:
                discount_list.append(item)
            no_discounted = len(discount_list)
            
    context = {
        'quse': quse,
        'items_no': items_no,
        'no_discounted': no_discounted,
        'form': form,
        'error': error,
    }
    
    return render(request, 'ceny/main.html', context)

class CenyDeleteView(DeleteView):
    model = Ceny
    template_name = 'ceny/confirm_del.html'
    success_url = reverse_lazy('home')
    
def update_prices(request):
    quse = Ceny.objects.all()
    for link in quse:
        link.save()
    return redirect('home')       
    

# Create your views here.
