from django.db import models


class Faq(models.Model):
    order = models.PositiveSmallIntegerField(verbose_name=u'Номер вопроса')
    question = models.CharField(max_length=200, verbose_name=u'Текст вопроса')
    answer = models.TextField(verbose_name=u'Текст ответа')
    helper_image = models.ImageField(upload_to='faq_uploads/',
                                     verbose_name=u'Изображение-помощь для приложения к ответу', blank=True)
    helper_file = models.FileField(upload_to='faq_uploads/',
                                   verbose_name=u'Файл-помощь для приложения к ответу', blank=True)

    class Meta:
        unique_together = ['order']
        verbose_name = u'Faq'
        verbose_name_plural = u'faq'

    """docstring for ClassName"""

    def __str__(self):
        return self.question
