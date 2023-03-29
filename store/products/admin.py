from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    Category,
    Brand,
    Product,
    Image,
    Color,
    Size,
    Review,
    Wishlist
    )


class ImgInline(admin.TabularInline):
    model = Image
    max_num = 6
    extra = 1


class ColorInline(admin.TabularInline):
    model = Color
    max_num = 6
    extra = 1
    

class SizeInline(admin.TabularInline):
    model = Size
    max_num = 6
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin,admin.ModelAdmin):
    inlines = [ImgInline, ColorInline, SizeInline]



@admin.register(Review)
class ProductReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Wishlist)
