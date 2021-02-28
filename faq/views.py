from django.shortcuts import render
from faq.models import Faq

def faq_view(request):
	""" Сервис, который генерирует FAQ сайта """
	faq = Faq.objects.all().order_by('order')
	
	context = {
	'faq':faq
	}

	return render(request, 'faq/faq.html', context = {'map' : context})