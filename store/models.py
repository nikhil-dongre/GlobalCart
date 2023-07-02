from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(max_length=300)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products',)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.product_name
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(vatiation_category = 'color',is_active = True)
    def size(self):
        return super(VariationManager, self).filter(vatiation_category = 'size',is_active = True)
    
    
variation_categories_choice = (
    ('color', 'color'),
    ('size', 'size')
)

class Variation(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    vatiation_category = models.CharField(max_length=100 ,choices=variation_categories_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()


    def __str__(self):
        return self.variation_value

    


