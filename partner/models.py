# models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_cleanup import cleanup
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager
from django_resized import ResizedImageField

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')
#category
class Category(models.Model):
    category_text = models.CharField(max_length=200)
   
    def __str__(self):
        return self.category_text

# parter model
@cleanup.select
class Partners(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )

    partner_name = models.CharField(max_length=250)
   
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    pic = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE)
    #body = models.TextField()
    descriptions=CKEditor5Field('Text', config_name='extends')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    image = ResizedImageField(force_format="WEBP", quality=75,upload_to='media/partner/%Y/%m/%d/') 
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    tags = TaggableManager()
    adreess = models.CharField(max_length=250)
    phone = models.CharField(max_length=30)
    account_number = models.FloatField()
    tax=models.FloatField
    percentage=models.FloatField()


    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.partner_name
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    def get_absolute_url(self):
        return reverse('partner:partner_detail',args=[self.slug])


    

