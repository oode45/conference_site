from django.db import models
import datetime
from django.contrib.auth import models as user


class RegistrationStatus(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    REGISTRATION_STATUS = [
        (ACTIVE, 'Открыта'),
        (INACTIVE, 'Закрыта'),
    ]

    is_active = models.CharField(
        max_length=50,
        choices=REGISTRATION_STATUS,
        default=True,
        verbose_name=u'Статус регистрации',
    )
    registration_inactive_text = models.TextField(verbose_name=u'Текст при закрытии регистрации на конференцию')

    class Meta:
        verbose_name = u'Статус регистрации'
        verbose_name_plural = u'Статус регистрации'

    def __str__(self):
        return self.get_is_active_display()


class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Название')

    class Meta:
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Название секции')
    number = models.PositiveSmallIntegerField(verbose_name=u'Номер секции')

    class Meta:
        verbose_name = u'Секция'
        verbose_name_plural = u'Секции'

    def __str__(self):
        return self.name


def paper_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Paper
    return 'manuscript_uploads/{0}/Section{1}/{2}_{3}_({4})'.format(
        datetime.datetime.now().year,
        instance.section.number,
        instance.last_name,
        instance.first_name[0],
        # datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename,
    )


def chief_review_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Paper
    return 'manuscript_uploads/{0}/Section{1}/{2}_{3}_(review {4}_{5})_{6}'.format(
        datetime.datetime.now().year,
        instance.section.number,
        instance.last_name,
        instance.first_name[0],
        # datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        instance.chief_last_name,
        instance.chief_first_name[0],
        filename,
    )

def reviewer_paper_upload(instance, filename):
    # file will be uploaded to MEDIA_ROOT/Paper
    return 'manuscript_uploads/{0}/Section{1}/reviewed_by_{2}_{3}'.format(
        datetime.datetime.now().year,
        instance.section.number,
        instance.reviewer,
        filename
    )


class Participant(models.Model):
    BACHELOR = 'Bachelor'
    MASTER = 'Master'
    POSTGRAD = 'Postgrad'
    SPECIALIST = 'Specialist'
    DOCTORAL = 'Doctoral'
    OTHER = 'Other'

    STATUSES = [
        (BACHELOR, 'Бакалавриат'),
        (MASTER, 'Магистратура'),
        (POSTGRAD, 'Аспирантура'),
        (SPECIALIST, 'Специалитет'),
        (DOCTORAL, 'Докторантура (PhD)'),
        (OTHER, 'Другое'),
    ]

    PARTICIPATION_TYPE = [
        ('oral', 'Устный'),
        ('poster', 'Постерный'),
    ]

    STATUS_TYPE = [
        ('approval', 'На рассмотрении'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]

    last_name = models.CharField(max_length=50, verbose_name=u'Фамилия участника')
    first_name = models.CharField(max_length=50, verbose_name=u'Имя участника')
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'Отчество участника')

    age = models.PositiveSmallIntegerField(verbose_name=u'Возраст')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=u'Страна')
    current_status = models.CharField(
        max_length=50,
        choices=STATUSES,
        default=BACHELOR,
        verbose_name=u'Текущая квалификация',
    )

    phone = models.CharField(max_length=50, verbose_name=u'Телефон')
    email = models.EmailField(verbose_name=u'Электронная почта')
    organization = models.CharField(max_length=200, verbose_name=u'Организация/учебное заведение')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name=u'Секция')
    participation_type = models.CharField(
        max_length=50,
        choices=PARTICIPATION_TYPE,
        default='oral',
        verbose_name=u'Вид доклада'
    )

    paper_name = models.CharField(max_length=300, verbose_name=u'Название доклада')
    paper_file = models.FileField(verbose_name=u'Файл доклада', upload_to=paper_upload)
    author_list = models.CharField(max_length=300, verbose_name=u'Список авторов')

    chief_last_name = models.CharField(max_length=50, null=True, blank=True,
                                       verbose_name=u'Фамилия научного руководителя')
    chief_first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'Имя научного руководителя')
    chief_middle_name = models.CharField(max_length=50, null=True, blank=True,
                                         verbose_name=u'Отчество научного руководителя')
    chief_phone = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'Телефон научного руководителя')
    chief_email = models.EmailField(null=True, blank=True, verbose_name=u'Электронная почта научного руководителя')
    chief_organization = models.CharField(max_length=200, null=True, blank=True,
                                          verbose_name=u'Организация/учебное заведение научного руководителя')
    chief_position = models.CharField(max_length=200, null=True, blank=True,
                                      verbose_name=u'Должность научного руководителя')

    chief_degree = models.CharField(max_length=200, null=True, blank=True,
                                      verbose_name=u'Степень/звание научного руководителя')

    chief_review = models.FileField(verbose_name=u'Файл отзыва', null=True, blank=True, upload_to=chief_review_upload)
    registration_date = models.DateField(auto_now_add=True, verbose_name=u'Дата регистрации')


    reviewer = models.ForeignKey(user.User, on_delete=models.CASCADE, blank=True, null=True)
    reviewer_accepted_toreview = models.DateField(verbose_name="Принял к рассмотрению", blank=True, null=True)
    reviewer_accepted = models.DateField(verbose_name="Принял", blank=True, null=True)
    reviewer_rejected = models.DateField(verbose_name="Отказал", blank=True, null=True)
    reviewer_corrected_manuscript = models.FileField(verbose_name="Расмотренная статья", blank=True, null=True, upload_to=reviewer_paper_upload)
    reviewer_corrected_manuscript_pdf = models.FileField(verbose_name="Расмотренная статья в .pdf", blank=True, null=True, upload_to=reviewer_paper_upload)



    status_type = models.CharField(
        max_length=50,
        choices=STATUS_TYPE,
        default='approval',
        verbose_name=u'Статус заявки'
    )

    class Meta:
        verbose_name = u'Участник'
        verbose_name_plural = u'Участники'

    def __str__(self):
        if not self.middle_name:
            return '{} {}.'.format(self.last_name, self.first_name[0].upper())
        else:
            return '{} {}.{}'.format(self.last_name, self.first_name[0].upper(), self.middle_name[0].upper())
