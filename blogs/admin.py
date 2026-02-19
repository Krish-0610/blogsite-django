from django.contrib import admin
from .models import Category, Blog


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug': ('title',)}
    list_display=('title', 'category', 'author', 'is_featured', 'status')
    search_fields=('id', 'title','status', 'category__category_name')
    list_editable=('is_featured',)

# Register your models here.
admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)