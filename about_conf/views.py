from django.shortcuts import render
from .models import Conference


def conference_info(request, template_name):
    """ Сервис, который генерирует страницы: описание сайта, важных дат, требований к оформлению, 
    контактов, группой оргкомитета и программой конференции """

    conference = Conference.objects.all()[0]

    if template_name == 'about.html':
        context = context_format('about', conference=conference)

    if template_name == 'important_dates.html':
        context = context_format('important_dates', conference=conference)

    if template_name == 'instructions.html':
        context = context_format('instructions', 'instructions_file', 'pattern_file', conference=conference)

    if template_name == 'contacts.html':
        context = context_format('image_station', 'map_image', 'contacts',  'academic_secretary_image', 
            'academic_secretary_info', 'map_source_name1', 'map_source_url1','map_source_name2', 'map_source_url2', conference=conference)

    if template_name == 'orgcom.html':
        context = context_format('chairman_photo', 'chairman_info', 'academic_secretary_image', 'academic_secretary_info',
            'committee_members', conference=conference)

    if template_name == 'program.html':
        context = context_format(conference=conference)

    return render(request, 'about_conf/' + template_name, context=context)

def context_format(*args, conference):  
    """ Формирование контекста для разных страниц """  
    context = {}
    for property in args:
        context[property] = getattr(conference, property)    
    return context

