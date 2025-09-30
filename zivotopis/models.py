from django.conf import settings 
from django.db import models
from django.utils import timezone 

# Importy pre Wagtail
#from wagtail.models import Page
#from wagtail.admin.panels import FieldPanel, MultiFieldPanel
#from wagtail.images.models import Image

CATEGORY_CHOICES = [
    ('bio', 'O mne'),
    ('trip', 'Výlet'),
    ('tech', 'IT'),
]

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='bio')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    images = models.ManyToManyField('Image', related_name='posts', blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class Image(models.Model):
    post = models.ForeignKey(Post, related_name='post_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    def __str__(self):
        return f"Obrázok pre post: {self.post.title}"

class Email(models.Model):
    sender_name = models.CharField(max_length=100, verbose_name="Vaše meno (povinné):")
    sender_email = models.EmailField(verbose_name="Váš email (povinné):")
    subject = models.CharField(max_length=200, verbose_name="Predmet:")
    message = models.TextField(verbose_name="Správa:")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject
    
class GalleryItem(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    
#class HomePage(Page):
#    intro_image = models.ForeignKey(
#        'wagtailimages.Image',
#        null=True,
#        blank=True,
#        on_delete=models.SET_NULL,
#        related_name='+'
#    )
#    
#    introduction = models.TextField(blank=True)
#    name_picture = models.TextField(blank=True)
#
#    content_panels = Page.content_panels + [
#        FieldPanel('intro_image'),
#        FieldPanel('introduction'),
#        FieldPanel('name_picture'),
#    ]

# Create your models here.
