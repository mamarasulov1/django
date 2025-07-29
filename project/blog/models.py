from django.db import models

# Create your models here.


class Catygory(models.Model):

    title = models.CharField(
        verbose_name="Заголовок",
        max_length=100,
    )

    class Meta:
        verbose_name = "катигория"
        verbose_name_plural = "катигория"

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(
        verbose_name="Тег",
        max_length=100
    )
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Тег"
        
    def __str__(self):
        return self.name
    
    
class News(models.Model):
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=100,
    )
    category=models.ForeignKey(
            Catygory,
            on_delete=models.CASCADE,
            related_name="news",
            verbose_name="Кат",
        )
    tags = models.ManyToManyField(
        Tag,
        related_name="news",
        verbose_name="Теги",
        blank=True,
        null=True
    )
    descriptions = models.TextField(
        verbose_name="описание",
        blank=True,
        null=True,
        default="по умол. описание",
    )
    date = models.DateTimeField(
        verbose_name='дата добавление',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        verbose_name='дата изменение',
        auto_now=True
    )
    author = models.CharField(
        max_length=50,
        verbose_name='автор',
        null=True,
        blank=True
    )
    views = models.PositiveIntegerField(
        verbose_name='просмотры',
        default=0
    )
    is_published = models.BooleanField(
        verbose_name='публичность',
        default=True
    )
    image = models.ImageField(
        "фото", 
        upload_to="news/photos", 
        blank=True, 
        null=True
        )

    class Meta:
        verbose_name = "новости"
        verbose_name_plural = "новости"
        
    @property
    def main_image(self):
        return self.images.first()


    def __str__(self):
        return self.title
    
    
class NewsImage(models.Model):
    news = models.ForeignKey(
        News, 
        on_delete=models.CASCADE, 
        related_name="images",
        verbose_name="новости"
    )
    image = models.ImageField(
        "фото", 
        upload_to="news/photos", 
        blank=True, 
        null=True
        )

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"
        
    # def __str__(self):
    #     return self.title
