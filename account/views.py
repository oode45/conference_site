from django.shortcuts import render, redirect, get_object_or_404
from participant_registration.models import Participant
from participant_registration.models import Section
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import AcceptForm, RejectForm
from datetime import datetime
import json
from conference_site import settings
from about_conf.models import Conference
from django.core.mail import send_mail, EmailMessage


def my_login(request):
    """ Сервис входа в учетную запись редактора и редирект на список свободных докладов"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(user=user, request=request)
            return redirect('all_manuscripts')
        else:
            return redirect('account')
    else:
        if request.user.is_active:
            return redirect('all_manuscripts')
        else:
            return render(request, 'account/login.html')


def my_logout(request):
    """ Сервис выхода из учетной записи и закрытия сессии"""
    request.session.clear()
    return redirect('account')


def accept(request, id):
    """ Сервис для принятия заявки участника """
    form = AcceptForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            accept_or_reject_post_req(request, id, form, 1, 'Принятие заявки')
        return redirect('my_manuscripts')
    else:
        context = accept_or_reject_get_req(request, id, AcceptForm, 'comment_accepted')
        if context is not None:
            return render(request, 'account/accept.html', context=context)
        else:
            return redirect('my_manuscripts')

def reject(request, id):
    """ Сервис для отклонения заявки участника """
    form = RejectForm(request.POST, request.FILES)    
    if request.method == 'POST':         
        if form.is_valid():
            accept_or_reject_post_req(request, id, form, 2, 'Отклонение заявки')
        return redirect('my_manuscripts')
    else:
        context = accept_or_reject_get_req(request, id, RejectForm, 'comment_rejected')
        if context is not None:            
            return render(request, 'account/reject.html', context=context)
        else:
            return redirect('my_manuscripts')

@login_required(login_url='account')
def my_manuscripts(request):
    """ Сервис отображения всех докладов редактора """
    if request.method == 'POST':
        return render(request, 'account/my_manuscripts.html')
    else:
        reviewer = request.user.participant_set.all()
        context = {'reviewer': reviewer}
        return render(request, 'account/my_manuscripts.html', context=context)


@login_required(login_url='account')
# """ Сервис, который отображает список всех участников без редактора и привязывает выбранные к текущему аккаунту редактора """
def all_manuscripts(request):
    if request.method == 'POST':
        save_manuscripts_to_reviewer(request)
        return redirect('my_manuscripts')
    else:
        sections_and_participants = display_all_free_reports()
        return render(request, 'account/all_manuscripts.html',
                      context={'sections_and_participants': sections_and_participants})

def display_all_free_reports():
    """ Возвращает всех участников в секции без редактора """
    sections_and_participants = []
    for section in Section.objects.all().order_by('number'):
        participants_in_section = section.participant_set.all().filter(reviewer=None).order_by('last_name')
        if len(participants_in_section) != 0:
            sections_and_participants.append([section, participants_in_section])
    return sections_and_participants    

def accept_or_reject_get_req(request, id, form, comment):
    """ Принятие или отклонение при GET запросе """
    participant = get_object_or_404(Participant, pk=id)
    if participant.status_type == 'approval' and participant.reviewer == request.user:
        form = form(initial={
            'comment': getattr(Conference.objects.all()[0], comment).format(participant, participant.paper_name)})
        context = {'id': id, 'participant': participant, 'form': form, } 
        return context


def accept_or_reject_post_req(request, id, form, num_of_status, expression):
    """ TПринятие или отклонение при POST запросе """
    manuscript = request.user.participant_set.all().get(id=id)
    manuscript.status_type = Participant.STATUS_TYPE[num_of_status][0]
    manuscript.reviewer_accepted = datetime.now()

    if num_of_status == 1:
        reviewer_corrected_manuscript = form.cleaned_data['reviewer_corrected_manuscript']
        reviewer_corrected_manuscript_pdf = form.cleaned_data['reviewer_corrected_manuscript_pdf']
        manuscript.reviewer_corrected_manuscript = reviewer_corrected_manuscript
        manuscript.reviewer_corrected_manuscript_pdf = reviewer_corrected_manuscript_pdf

    write_reviewer_reply(manuscript.last_name, manuscript.reviewer.username, expression,
                         form.cleaned_data['comment'])
    # Gmail does not accept letters from the local machine. Don't forget to uncomment on the server.
    # gmail_response(recipient=manuscript.email, message_title=expression,
    #                 message_body=form.cleaned_data['comment'])
    manuscript.save()

def write_reviewer_reply(recipient, reviewer, message_title, message_body):
    """ Логирование ответа редактора """
    message = {"from": reviewer, "to": recipient,
               "title": message_title, "message": message_body}
    with open('{}\\answers_upload\\from_{}-to_{}.json'.format(settings.MEDIA_ROOT, reviewer, recipient), 'w') as file:
        json.dump(message, file)

def gmail_response(recipient, message_title, message_body):
    """ Ответ участнику от редактора письмом """
    res = EmailMessage(subject=message_title,
                       body=message_body, to=[recipient]).send()

def save_manuscripts_to_reviewer(request):
    """ Привязка выбранных участников к текущему аккаунту редактора """
    pappers = request.POST.getlist('selected_paper')
    for id_participant in pappers:
        participant = Participant.objects.all().get(id=id_participant)
        participant.reviewer = request.user
        participant.reviewer_accepted_toreview = datetime.now()
        participant.save()
