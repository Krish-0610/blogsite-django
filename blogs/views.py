from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Blog, Category

# Create your views here.
def posts_by_category(request, category_id):
    posts = Blog.objects.filter(status='Published', category=category_id)

    #> Use this when you want to show 404 error page on id not found
    category = get_object_or_404(Category, pk=category_id)

    # >Use try/catch when we want to do some custom action if fails
    # try:
    #     category = Category.objects.get(pk=category_id)
    # except:
    #     # redirect to home page
    #     return redirect('home')
    context = {
        'posts':posts,
        'category': category

    }
    return render(request, 'post_by_category.html',context)