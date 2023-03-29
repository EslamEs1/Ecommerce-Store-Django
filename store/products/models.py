from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from utils.utils import slugify_instance_title
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    font = models.CharField(max_length=50, default=False)
    slug = models.SlugField(max_length=50, editable=False)

    class Meta:
        ordering = ['-title']
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
        
        
class Brand(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, editable=False)

    class Meta:
        ordering = ['-title']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Brand, self).save(*args, **kwargs)
        


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product_category',on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='product_brand',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='store/img/products')
    slug = models.SlugField(max_length=200, editable=False)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    old_price = models.DecimalField(max_digits=19, decimal_places=2)
    content = models.TextField()
    specification = models.TextField()
    tags = TaggableManager()
    available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])
    
    def star(self):
        ratings = self.reviews.all()
        if ratings:
            return round(sum(r.rating for r in ratings) / len(ratings), 2)
        else:
            return 0
    
        
        
@receiver(pre_save, sender=Product)
def check_slug(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)


@receiver(post_save, sender=Product)
def course_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)
        
        

class Size(models.Model):
    product = models.ForeignKey(Product, related_name='size', on_delete=models.CASCADE)
    size = models.CharField(max_length=50)

    class Meta:
        ordering = ['-size']
    
    def __str__(self):
        return self.size


class Color(models.Model):
    product = models.ForeignKey(Product, related_name='color', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)

    class Meta:
        ordering = ['-color']
    
    def __str__(self):
        return self.color


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='store/img/products')

    def __str__(self):
        return self.product.title + 'image'
    class Meta:
        ordering = ['-img']


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_reviews', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title
    
    class Meta:
        ordering = ['-created_at']


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
