from django import forms
from .models import Country, Section, Participant
from captcha.fields import CaptchaField
from .validators import *
from django.core.validators import RegexValidator
import re



def get_contries():
    countries = [(country.pk, country.name) for country in Country.objects.all()]
    return countries


def get_section():
    sections = [(section.pk, section.name) for section in Section.objects.all()]
    return sections


class RegistrationForm(forms.Form):
    last_name = forms.CharField(label='Фамилия', max_length=50, validators=[validate_first_name])
    first_name = forms.CharField(label='Имя', max_length=50, validators=[validate_last_name])
    middle_name = forms.CharField(label='Отчество', max_length=50, required=False, validators=[validate_middlename])
    current_status = forms.ChoiceField(choices=Participant.STATUSES, label='Текущая квалификация')
    age = forms.IntegerField(max_value=39, min_value=18, label='Ваш возраст')
    phone = forms.CharField(label='Телефон', max_length=50, validators=[phone])
    email = forms.EmailField(label=u'Электронная почта')
    organization = forms.CharField(max_length=200, label=u'Организация/учебное заведение')
    country = forms.ChoiceField(choices=get_contries, label='Страна')
    section = forms.ChoiceField(choices=get_section, label=u'Секция')
    participation_type = forms.ChoiceField(choices=Participant.PARTICIPATION_TYPE, label=u'Вид доклада')

    paper_name = forms.CharField(max_length=300, label=u'Название доклада')
    author_list = forms.CharField(max_length=300, label=u'Список авторов', validators=[
        RegexValidator(regex='[а-яА-Я\\s.,]+$', message='Поле должно быть заполненно кириллицей и не должно содержать цирф и символов, кроме точек и запятых.')
        ])
    paper_file = forms.FileField(label=u'Файл статьи', validators=[extension_doc])    

    chief_last_name = forms.CharField(max_length=50, label=u'Фамилия', required=False)
    chief_first_name = forms.CharField(max_length=50, label=u'Имя', required=False)
    chief_middle_name = forms.CharField(max_length=50, label=u'Отчество', required=False)
    chief_phone = forms.CharField(max_length=50, label=u'Телефон', required=False)
    chief_email = forms.EmailField(label=u'Электронная почта', required=False)
    chief_organization = forms.CharField(
        max_length=200, label=u'Организация/учебное заведение', required=False)
    chief_position = forms.CharField(max_length=200, label=u'Должность', required=False)
    chief_degree = forms.CharField(max_length=200, label=u'Степень и/или звание', required=False)
    chief_review = forms.FileField(label=u'Файл отзыва', required=False)  


    def clean(self):
        cleaned_data = super().clean()
        msg = "Поле заполнено неправильно или пустое."
        current_status_s = cleaned_data.get("current_status")
        print("before")

        for participant in Participant.objects.all():
            if participant.status_type == 'approval' or participant.status_type == 'accepted':
                if str(cleaned_data.get('paper_name')).lower() == str(participant.paper_name).lower():
                    self.add_error('paper_name', 'Доклад с таким именем уже существует.')

        if current_status_s != Participant.OTHER:
            print("after")
            chief_last_name = cleaned_data.get("chief_last_name")
            if chief_last_name == '':
                print("ATENTION2")
                self.add_error('chief_last_name', msg)
            else:
                if not re.search('^[A-ЯЁ][а-яё\\s]+$', chief_last_name):
                    self.add_error('chief_last_name', "Фамилия указывается на русском языке с заглавной буквы. Например: Иванов")


            chief_first_name = cleaned_data.get("chief_first_name") 
            if chief_first_name == '':
                self.add_error('chief_first_name', msg) 
            else:
                if not re.search('^[A-ЯЁ][а-яё\\s]+$', chief_first_name):
                    self.add_error('chief_first_name', "Имя указывается на русском языке с заглавной буквы. Например: Иванов")

            chief_middle_name = cleaned_data.get("chief_middle_name") 
            if chief_middle_name != '' and not re.search('^[A-ЯЁ][а-яё\\s]+$', chief_middle_name):
                self.add_error('chief_middle_name', msg) 


            chief_phone = cleaned_data.get("chief_phone") 
            if chief_phone == '':
                self.add_error('chief_phone', msg)
            else:
                if not re.search('^[0-9+][0-9 ()-]+[0-9]$', chief_phone):
                    self.add_error('chief_phone', "Номер должен соотвествовать форме.")

            chief_email = cleaned_data.get("chief_email") 
            if chief_email == '':
                self.add_error('chief_email', msg) 

            chief_organization = cleaned_data.get("chief_organization") 
            if chief_organization == '':
                self.add_error('chief_organization', msg) 

            chief_position = cleaned_data.get("chief_position") 
            if chief_position == '':
                self.add_error('chief_position', msg) 

            chief_review = cleaned_data.get("chief_review") 
            if chief_review is None:
                self.add_error('chief_review', msg)
            else:
                if not re.search('[.pdf]{4}$',str(chief_review.name)):
                    self.add_error('chief_review', "Файл должен быть в формате .pdf")

            chief_degree = cleaned_data.get("chief_degree") 
            if chief_degree == '':
                self.add_error('chief_degree', msg)
            else:
                if not re.search('[а-яА-Я\\s.,-]+$',str(chief_degree)):
                    self.add_error('chief_degree', "Поле не должно содержать цирф и символов, кроме точек, запятых и дефисов")

    # status_type = forms.ChoiceField(choices=Participant.STATUS_TYPE, label=u'Статус заявки')


class CaptchaTestForm(forms.Form):
    captcha = CaptchaField(error_messages=dict(invalid='Неверная captcha. Повторите попытку'))
