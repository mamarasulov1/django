from django.shortcuts import render
from .models import News,Catygory,Tag

def news_list(request):
    news = News.objects.all()
    category = Catygory.objects.all() 
    tags = Tag.objects.all()
    context = {
        'news': news,
        'category': category,
        'tags': tags,
    }
    return render(request, 'blog/news.html', context=context)


def news_detail(request, id):
    news = News.objects.get(id=id)
    return render(request, 'blog/news_detail.html',context={"news":news})