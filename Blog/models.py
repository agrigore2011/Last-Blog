from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.urls import reverse

def generate_filename(instance,filename):
    filename=instance.slug+'.jpg'
    return "{0}/{1}".format(instance, filename)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post (models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))

    title = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(max_length=250, unique_for_date='published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(upload_to= generate_filename, verbose_name='Изображение')
    body = models.TextField(verbose_name='Содержание')
    text_min = models.CharField(max_length=300, verbose_name='Краткое описание')
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    dislikes = models.PositiveIntegerField(default=0, verbose_name='Дизлайки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    class Meta:
        ordering = ('-published',)

    def __str__(self):
         return self.title

    def get_absolute_url(self):
        return reverse('Blog:post_detail', args=[self.published.year, self.published.month, self.published.day, self.slug])