from django.contrib import admin
from .models import Product , Variation,ReviewRating
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','is_available','modified_date')
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_value','vatiation_category','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_value','vatiation_category')



admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)
