from django.shortcuts import render, redirect, get_object_or_404
from .models import News,Category,Tag,NewsImage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def registr_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('register_')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже есть')
            return redirect('register_')              
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Регистрация успешна! Теперь войдите.')
        return redirect('login_')
    return render(request, 'blog/registr.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('news-list')
        else:
            messages.error(request, 'Неверный логин или пароль')
            return redirect('login_')
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('login_')


@login_required
def news_list(request):
    news = News.objects.filter(is_published=True)
    categories= Category.objects.all()
    tags = Tag.objects.all()
    search = request.GET.get('search','')
    category_id = request.GET.get('category','')
    selected_tag_ids = request.GET.getlist('tags')
    selected_tag = []
    if search:
        news = news.filter(title__icontains=search)
    if category_id:
        try:
            category = Category.objects.get(id=int(category_id))
            news = news.filter(category=category)
        except (Category.DoesNotExist, ValueError):
            category = None
    else:
        category = None
    
    if selected_tag_ids:
        selected_tag = [int(tag) for tag in selected_tag_ids]
        news = news.filter(tags__in=selected_tag_ids)
        
    context = {
    'news': news,
    'categories': categories,
    'tags':tags,
    'search':search,
    'selected_category':category,
    'selected_tag':selected_tag
    }
    return render(request, 'blog/news.html', context=context)


def news_detail(request, id):
    news = get_object_or_404(News, id=id)
    return render(request, 'blog/news_detail.html',context={"news":news})

def news_Cat(request,id):
    category = Category.objects.get(id=id)
    categories = Category.objects.all() 
    news = News.objects.filter(category=category)
    context = {
        'news': news,
        'categories': categories,
        'selected_category':category
    }
    return render(request, 'blog/news.html', context=context)


def news_creat(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        tag_ids = request.POST.getlist('tags')
        images = request.FILES.getlist('images')
        category = Category.objects.get(id=category_id)

        news = News.objects.create(
            title=title,
            description=description,
            category=category,
            author = request.user.username,
            # views=viw
        )
        news.tags.set(tag_ids)

        for image in images:
            news.images.create(
                image=image
            )
        return redirect('news_detail', news.id)
    context = {
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/creat.html', context)


def tag_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Tag.objects.create(name=name)
        return redirect('news_creat')
    return render(request,'blog/tag_create.html')


def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(title=name)
            
        return redirect('news_creat')
    return render(request,'blog/category_create.html')


def change_view(request,id):
    news = News.objects.get(id=id)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        tag_ids = request.POST.getlist('tags')
        images = request.FILES.getlist('images')
        category = Category.objects.get(id=category_id)
        
        news.tags.set(tag_ids)
        news.title = title
        news.description = description
        news.category_id = category_id
        news.tag_ids = tag_ids
        news.images.set(images) 
        news.category = category

        news.tags.clear()
        news.tags.set(tag_ids)
        news.save()
        return redirect('news_detail', news.id)
    images = news.images.all()
    
    context={
            'news':news,
            'categories':categories,
            'tags':tags,
            'images': images
        }
    
    return render(request,'blog/change.html',context)

def change_image(request, id):
    img = NewsImage.objects.get(id=id)
    if request.method == 'POST':
        new_image = request.FILES.get('image')
        if new_image:
            img.image = new_image
            img.save()
            return redirect('change', img.news.id)
    context = {
        'img': img
    }
    return render(request, 'blog/change_image.html', context)


def add_image(request,id):
    news = News.objects.get(id=id)
    if request.method == 'POST':
        new_image = request.FILES.get('image')
        if new_image:
            NewsImage.objects.create(
                news=news,
                image=new_image
                )
            return redirect('change', news.id)
    context = {
        'news': news,
    }
    return render(request, 'blog/add_image.html', context)


def delete_img(request,id):
    imge = get_object_or_404(NewsImage,id=id)
    new_id = imge.news.id
    imge.delete()

    return redirect('change', new_id)
 
def delete_news(request,id):
    news = News.objects.get(id=id)
    if request.method == 'POST':
        news.delete()
    return redirect('news-list')
