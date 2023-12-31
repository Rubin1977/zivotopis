from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EmailForm
from django.contrib import messages
from django.core.mail import send_mail

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'zivotopis/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'zivotopis/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'zivotopis/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'zivotopis/post_edit.html', {'form': form})

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

#def send_email(request):
#    if request.method == "POST":
#        form = EmailForm(request.POST)
#        if form.is_valid():
#            form.save()
#            messages.success(request, "Email bol úspešne odoslaný!")
#            return redirect('success_view') 
#    else:
#        form = EmailForm()
#    return render(request, 'registration/send_email.html', {'form': form})

def success_view(request):
    return render(request, 'zivotopis/success.html')

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            adresa = 'ruzbacky@yahoo.com'
            predmet = 'Nová zpráva z životopis formulára!'
            meno = 'Meno odosielatela: ' + form.cleaned_data['sender_name']
            sprava = '\nSpráva: ' + form.cleaned_data['message'] 
            hlavicka = '\na jeho emailová adresa:\n' + form.cleaned_data['sender_email']
            hlavicka += "\nMIME-Version: 1.0\n"
            hlavicka += "Content-Type: text/html; charset=\"utf-8\"\n" 
            predmet_odosielatela = 'Predmet: ' + form.cleaned_data['subject']
            uspech = send_mail (predmet, 
                               form.cleaned_data['subject'], 
                               form.cleaned_data['sender_email'], 
                               [adresa], 
                               fail_silently=False, 
                               html_message=meno + hlavicka + predmet_odosielatela + sprava
                               )
            if uspech:
                messages.success(request, "Email bol úspešne odoslaný!")
                return redirect('success_view')
            else:
                messages.error(request, 'Email se nepodařilo odeslat. Zkontrolujte adresu.') 
    else:
        form = EmailForm()    
    return render(request, 'registration/send_email.html', {'form': form})

# Create your views here.
