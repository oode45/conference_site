from django.db import models

# Create your models here.


class Gallery(models.Model):
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    day = models.PositiveSmallIntegerField(verbose_name='День')
    zipfile = models.FileField(verbose_name='Zip-архив', upload_to='photogallery_images/', null=True,blank=True)

    class Meta:
        unique_together = [['year', 'day']]
        verbose_name = u'Фотогаллерея'
        verbose_name_plural = u'Фото'

    def __str__(self):
        return ('Год: {} - День: {}').format(self.year, self.day)


class Images(models.Model):
    post = models.ForeignKey(Gallery, default=None, on_delete=models.CASCADE, related_name='image_list')
    image = models.ImageField(upload_to='photogallery_images/',
                              verbose_name='Image')
