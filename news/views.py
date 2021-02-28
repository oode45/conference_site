from django.shortcuts import render, get_object_or_404
from news.models import News


def news_list(request):
    """ Сервис для отображения ленты новостей """
    news = News.objects.all().order_by('-posting_date')[:3]
    context = {
        'news': news,
    }

    return render(request, 'news.html', context)


def news_detail(request, id):
    """ Сервис для отображения полного текста новости """
    news_item = get_object_or_404(News, pk=id)
    context = {
        'news_item': news_item,
    }

    return render(request, 'news_detail.html', context)
