from django.db import models


class Archive(models.Model):
    name = models.CharField(max_length=200, verbose_name='Полное название сборника материалов')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска')
    issue = models.PositiveSmallIntegerField(verbose_name='Номер выпуска')

    class Meta:
        verbose_name_plural = u'Архив'

    """docstring for ClassName"""

    def __str__(self):
        return ('Год: {} - Номер: {}').format(self.year, self.issue)


class File(models.Model):
    post = models.ForeignKey(Archive, default=None, on_delete=models.CASCADE, related_name='archive_list')
    volume = models.PositiveSmallIntegerField(verbose_name='Том выпуска')
    proceedings_upload = models.FileField(upload_to='archive_uploads/', verbose_name='Полнотекстовая версия')


# Create your models here.
