from django.contrib import admin
from product_management.models import category,subcategory,product_master,product_image_master,product_price_history



# Register your models here.
class CategoryAdmin(category):
	fieldsets=fieldsets = [
        (None, {'fields': ('category_name')}),
        ]

admin.site.register(category, CategoryAdmin)
