from django.db import models
import datetime


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'Заголовок')
    content = models.TextField(verbose_name=u'Текст новости')
    posting_date = models.DateField(default=datetime.date.today, verbose_name=u'Дата публикации новости')
    thumbnail_image = models.ImageField(upload_to='news_images/', verbose_name=u'Фото миниатюры')
    image1 = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name=u'Фото1 для новости')
    image2 = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name=u'Фото2 для новости')
    image3 = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name=u'Фото3 для новости')

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'

    def __str__(self):
        return self.title
