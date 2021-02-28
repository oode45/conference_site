from django.contrib import messages
from django.shortcuts import render, redirect
from participant_registration.models import Participant, Country, Section, RegistrationStatus
from .forms import RegistrationForm
from .forms import CaptchaTestForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.core.files.storage import FileSystemStorage

def registration_form(request):
	""" Сервис для сохранения данных из формы или генерации пустой формы"""

	if request.method == 'POST':
		# Если POST и форма валидна, забираем данные из формы и сохраняем объект участника
		form = RegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			participant = save_participant_from_form(form)
			del request.session['valid_captcha']
			# process the data in form.cleaned_data as required
			# redirect to a new URL:
			message_text = 'Уважаемый/ая {} {}, ваш доклад "{}" принят на рассмотрение'.format(
				participant.last_name, participant.first_name, participant.paper_name)
			messages.add_message(request, messages.INFO, message_text)
			return redirect('status_claim')

	# Если GET и капча пройдена, то создаем пустую форму или направляем снова на капчу
	else:
		if RegistrationStatus.objects.all()[0].is_active == RegistrationStatus.ACTIVE:
			if 'valid_captcha' in request.session:
				form = RegistrationForm()
			else:
				return redirect('registration_captcha')
		else:
			return redirect('registration_inactive')

	return render(request, 'participant_registration/registration_form.html', {'form': form})


def registration_captcha(request):
	""" Сервис для генерации капчи """
	if request.method == 'POST':
		form = CaptchaTestForm(request.POST)
		if form.is_valid():
			request.session['valid_captcha'] = 'Yes'
			return redirect('registration_form')
	else:
		if RegistrationStatus.objects.all()[0].is_active == RegistrationStatus.ACTIVE:
			form = CaptchaTestForm()
		else:
			return redirect('registration_inactive')

	return render(request, 'participant_registration/registration_captcha.html', {'form': form})


def status_claim(request):
	""" Сервис для генерации страницы с зарегистрировавшимися участниками """
	sections_and_participants = get_sections_and_participants()
	return render(request, 'participant_registration/status.html', context={
		'sections_and_participants': sections_and_participants, })


def registration_inactive(request):
	""" Сервис для генерации страницы с неактивной регистрацией """
	status = RegistrationStatus.objects.all()[0]
	return render(request, 'participant_registration/registration_inactive.html', context={
		'status': status, })


@staff_member_required(login_url='/')
def statistics(request):
	""" Сервис, который формирует список email-ов участников конференции, список редакторов с 
	рассматриваемыми ими докладами, секции с участниками и списки с устными и постерными докладами """
	reviewers_and_participants = []
	sections = Section.objects.values_list('name', flat=True)
	reviewers = set()
	emails = Participant.objects.all().values_list('email', flat=True)
	reviewer_none  = Participant.objects.all().filter(reviewer = None).order_by('section')

	for participant in Participant.objects.all():
		if participant.reviewer != None:
			reviewers.add(participant.reviewer)

	for reviewer in reviewers:
		reviewers_and_participants.append([reviewer, reviewer.participant_set.all()])

	sections_and_participants = get_sections_and_participants(filter='oral')
	participation_type_poster = Participant.objects.all().filter(participation_type = 'poster', status_type='accepted').order_by('last_name')

	context = {
		'reviewers_and_participants': reviewers_and_participants,
		'emails':sorted(list(set(emails)), key=str.casefold),
		'sections_and_participants':sections_and_participants,
		'participation_type_poster':participation_type_poster,
		'poster_num': len(participation_type_poster),
		'reviewer_none':reviewer_none,
		'sections':sections,
	}
	return render(request, 'participant_registration/statistics.html', context=context)


@login_required(login_url='/')
def agenda(request):
	""" Сервис, который генерирует программу конференции (Логика пока в разработке) """
	sections_and_participants = get_sections_and_participants()
	return render(request, 'participant_registration/agenda.html', context={
		'sections_and_participants': sections_and_participants, })


def get_sections_and_participants(filter=None):
	""" Возвращает секции с участниками, отсортированными и отфильтрованными по нужным полям """
	sections_and_participants = []
	for section in Section.objects.all().order_by('number'):
		if filter is None:
			participants_in_section = section.participant_set.all().order_by('last_name')
			sections_and_participants.append([section, participants_in_section])
		else:
			participants_in_section_oral = section.participant_set.all().filter(participation_type = 'oral', status_type='accepted').order_by('last_name')
			count = len(participants_in_section_oral)
			sections_and_participants.append([section, participants_in_section_oral, count])
	return sections_and_participants




def save_participant_from_form(form):
	""" Сохранение объекта участника с информацией из полей формы """	
	last_name = form.cleaned_data['last_name']
	first_name = form.cleaned_data['first_name']
	middle_name = form.cleaned_data['middle_name']
	current_status = form.cleaned_data['current_status']
	age = form.cleaned_data['age']
	phone = form.cleaned_data['phone']
	email = form.cleaned_data['email']
	organization = form.cleaned_data['organization']
	country_id = form.cleaned_data['country']
	section_id = form.cleaned_data['section']
	participation_type = form.cleaned_data['participation_type']
	paper_name = form.cleaned_data['paper_name']
	author_list = form.cleaned_data['author_list']
	paper_file = form.cleaned_data['paper_file']
	chief_last_name = form.cleaned_data['chief_last_name']
	chief_first_name = form.cleaned_data['chief_first_name']
	chief_middle_name = form.cleaned_data['chief_middle_name']
	chief_phone = form.cleaned_data['chief_phone']
	chief_email = form.cleaned_data['chief_email']
	chief_organization = form.cleaned_data['chief_organization']
	chief_position = form.cleaned_data['chief_position']
	chief_degree = form.cleaned_data['chief_degree']
	chief_review = form.cleaned_data['chief_review']

	p = Participant(
		last_name=last_name,
		first_name=first_name,
		middle_name=middle_name,
		current_status=current_status,
		age=age,
		phone=phone,
		email=email,
		organization=organization,
		country=Country.objects.get(pk=country_id),
		section=Section.objects.get(pk=section_id),
		participation_type=participation_type,
		paper_name=paper_name,
		author_list=author_list,
		paper_file=paper_file,

		chief_last_name=chief_last_name,
		chief_first_name=chief_first_name,
		chief_middle_name=chief_middle_name,
		chief_phone=chief_phone,
		chief_email=chief_email,
		chief_organization=chief_organization,
		chief_position=chief_position,
		chief_degree=chief_degree,
		chief_review=chief_review,
	)

	p.save()
	return p
