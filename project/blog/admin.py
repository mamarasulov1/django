from django.contrib import admin
from .models import News, Category, NewsImage,Tag
from django.utils.safestring import mark_safe

# Register your models here.



class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 0

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'is_published', 'views', 'get_image']
    readonly_fields = ['get_image']
    inlines = [NewsImageInline]
    
    
    @admin.display(description='Изображение')
    def get_image(self, news):
        return mark_safe(f'<img src={news.main_image.image.url if news.main_image else "-"} width="150px" />')

    # @admin.display(description='Изображение')
    # def get_image(self, news):
    #     if news.image:
    #         return mark_safe(f'<img src="{news.image.url}" width="150px" />')
    #     return "-"


class NewsInline(admin.TabularInline):
    model = News
    extra = 0
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [NewsInline]
    
# @admin.register(NewsImage)
# class NewsImage(admin.ModelAdmin):
#     list_display = ['news__title', 'get_image']
    
#     @admin.display(description='Изображение')
#     def get_image(self, news):
#         return mark_safe(f'<img src={news.image.url if news.image else "-"} width="150px" />')

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ['get_news_title', 'get_image']
    
    def get_news_title(self, obj):
        return obj.news.title
    get_news_title.short_description = 'Новость'

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="150px" />') if obj.image else "-"
    get_image.short_description = 'Изображение'


@admin.register(Tag)
class Tag(admin.ModelAdmin):
    pass 

