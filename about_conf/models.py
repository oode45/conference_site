from django.db import models


class Conference(models.Model):

# """ Общие сведения о конференции """

    important_dates = models.TextField(verbose_name=u'Важные даты')

    about = models.TextField(verbose_name=u'О конференции')

# Контакты
    image_station = models.ImageField(upload_to='contacts_images/', verbose_name=u'Фото Станции')
    map_image = models.ImageField(upload_to='contacts_images/', 
                                  verbose_name=u'Карта с расположением станции')
    contacts = models.TextField(verbose_name=u'Контакты')
    academic_secretary_image = models.ImageField(
        upload_to='contacts_images/', verbose_name=u'Фото ученого секретаря')
    academic_secretary_info = models.TextField(verbose_name=u'Данные ученого секретаря')
    map_source_name1 = models.CharField(max_length=200, verbose_name=u'Подпись ссылки на карту геолокации 1')
    map_source_url1 = models.URLField(max_length=300, verbose_name=u'Ссылка на карту геолокации 1')
    map_source_name2 = models.CharField(max_length=200, verbose_name=u'Подпись ссылки на карту геолокации 2')
    map_source_url2 = models.URLField(max_length=300, verbose_name=u'Ссылка на карту геолокации 2')

# Требования к оформлению
    instructions = models.TextField(verbose_name=u'Текст требований к оформлению')
    instructions_file = models.FileField(
        verbose_name=u'Файл требований к оформлению', upload_to='for_authors_uploads/')
    pattern_file = models.FileField(
        verbose_name=u'Файл-шаблон оформления статьи', upload_to='for_authors_uploads/', blank=True,null=True)

# Оргкомитет
    chairman_photo = models.ImageField(upload_to='orgcom_images/', verbose_name='Фото председателя')
    chairman_info = models.TextField(verbose_name='Текст подписи для председателя')
    committee_members = models.TextField(verbose_name='Члены оргкомитета')

# Шаблоны принятия\отклонения заявок
    comment_accepted = models.TextField(verbose_name='Текст комментария для принятия', null=True)
    comment_rejected = models.TextField(verbose_name='Текст комментария для отклонения', null=True)

    class Meta:
        verbose_name = u'Информация о конференции'
        verbose_name_plural = u'Информация'

    def __str__(self):
        return self.about[:30]
