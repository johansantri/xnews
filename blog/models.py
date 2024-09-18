# models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_cleanup import cleanup
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')
#category
class Category(models.Model):
    category_text = models.CharField(max_length=200)
   
    def __str__(self):
        return self.category_text

# post model
@cleanup.select
class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
   
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    category = models.ForeignKey(Category, related_name="blog_posts", on_delete=models.CASCADE)
    #body = models.TextField()
    body=CKEditor5Field('Text', config_name='extends')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/featured_image/%Y/%m/%d/') 
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    tags = TaggableManager() 
    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.slug])
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

    

# comment model    
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    name=models.CharField(max_length=50)
    email=models.EmailField()
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)