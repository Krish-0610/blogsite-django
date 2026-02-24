from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import PermissionDenied
from .forms import BlogPostForm, CategoryForm, AddUserForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your views here.
@permission_required('blogs.view_blog', raise_exception=True)
def dashboard(request):
    category_count = Category.objects.all().count()
    blog_count = Blog.objects.all().count()

    context = {
        'category_count':category_count,
        'blog_count':blog_count,
    }

    return render(request, 'dashboard/dashboard.html', context)

@permission_required('blogs.view_category', raise_exception=True)
def categories(request):
    return render(request, 'dashboard/categories.html')

@permission_required('blogs.add_category', raise_exception=True)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories")
    else:
        form = CategoryForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/add_category.html', context)

@permission_required('blogs.change_category', raise_exception=True)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories")
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category':category
    }

    return render(request, 'dashboard/edit_category.html', context)

@permission_required('blogs.delete_category', raise_exception=True)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    
    return redirect('categories')

@permission_required('blogs.view_blog', raise_exception=True)
def posts(request):
    posts = Blog.objects.all()
    context = {
        'posts':posts
    }

    return render(request, 'dashboard/posts.html', context)

@permission_required('blogs.add_blog', raise_exception=True)
def add_post(request):
    if request.method=='POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # Temporarily saving the form (Instance of Blog model)
            post.author = request.user
            post.save() # To use the post.id into slug
            title = form.cleaned_data['title']
            post.slug = slugify(title)+'-'+str(post.id)
            post.save()
            return redirect('posts')
    else:
        form = BlogPostForm()

    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_post.html', context)

@permission_required('blogs.change_blog', raise_exception=True)
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title)+'-'+str(post.id)
            post.save()
            return redirect("posts")
    else:
        form = BlogPostForm(instance=post)

    context = {
        'form': form,
        'post':post
    }
    return render(request, 'dashboard/edit_post.html', context)

@permission_required('blogs.delete_blog', raise_exception=True)
def delete_post(request, pk):
    post= get_object_or_404(Blog, pk=pk)
    post.delete()

    return redirect('posts')

@permission_required('auth.view_user',raise_exception=True)
def users(request):
    users = User.objects.all()
    context = {
        'users':users,
    }
    return render(request, 'dashboard/users.html', context)

@permission_required('auth.add_user',raise_exception=True)
def add_user(request):
    if request.method=='POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = AddUserForm()

    context = {
        'form':form,
    }
    return render(request, 'dashboard/add_user.html', context)

@permission_required('auth.change_user',raise_exception=True)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method=='POST':
        form=EditUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form=EditUserForm(instance=user)

    context={
        'form':form,
        'user':user,
    }

    return render(request, 'dashboard/edit_user.html', context)

@permission_required('auth.delete_user',raise_exception=True)
def delete_user(request, pk):
    user= get_object_or_404(User, pk=pk)
    if user.is_superuser:
        if request.user.is_superuser:
            user.delete()
        else:
            raise PermissionDenied("You are not allow to delete this user")
    else:
        user.delete()

    return redirect('users')