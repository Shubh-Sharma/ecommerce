from django.contrib import admin

# Register your models here.


from .models import Product, Variation, ProductImage, Category, ProductFeatured

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1
	max_num = 6


class VariationInLine(admin.TabularInline):
	model = Variation
	extra = 1
	max_num = 6


class ProductAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'price']
	inlines = [
		ProductImageInline,
		VariationInLine,
	]
	class Meta:
		model = Product


admin.site.register(Product, ProductAdmin)

# admin.site.register(Variation)

# admin.site.register(ProductImage)

admin.site.register(Category)

admin.site.register(ProductFeatured)