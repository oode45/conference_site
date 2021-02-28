from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.translation import gettext_lazy as _ 


def validate_first_name(text):
    validators.RegexValidator(regex = '^[A-ЯЁ][а-яё\\s]+$', message='Фамилия указывается на русском языке с заглавной буквы. Например: Иванов')(text)

def validate_last_name(text):
    validators.RegexValidator(regex = '^[A-ЯЁ][а-яё\\s]+$', message='Имя указывается на русском языке с заглавной буквы. Например: Иван')(text)

def validate_middlename(text):
	if text is not None:
		validators.RegexValidator(regex = '^[A-ЯЁ][а-яё\\s]+$', message='Отчество указывается на русском языке с заглавной буквы. Например: Иванович')(text)


def age(text):
	try:
		if (int(text)<18 or int(text)>90):
			raise ValidationError(message='Возраст должен быть в пределах от 18 до 90')

	except ValueError as e:
		raise ValidationError(message='Возраст должен быть в пределах от 18 до 90')
	
		
	
def phone(text):
 	# validators.RegexValidator(regex = '^[0][0-9]{3}\\s[0-9]{3}[-][0-9]{3}$', message='Введите номер в требуемом формате')(text)
 	v = validators.RegexValidator(regex = '^[0-9+][0-9 ()-]+[0-9]$', message='Введите номер в требуемом формате')
 	v(text)


def extension_doc(text):
 	validators.FileExtensionValidator(allowed_extensions=['doc', 'docx'], message='Файл доклада должен быть в формате Word (*.doc или *.docx)')(text)


def extension_pdf(text):
 	validators.FileExtensionValidator(allowed_extensions=['pdf'], message='Отзыв должен быть в формате pdf')(text)



