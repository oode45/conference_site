from django.shortcuts import render
from photogallery.models import Gallery
# Create your views here.


def photogallery_view(request):
    """ Сервис для генерации фотогаллерей по годам """
    photogallery_list, days, archives = get_photolist_days_archives(Gallery)

    context = {
        'photogallery_list': photogallery_list,
        'days': days,
        'archives':archives,
    }

    return render(request, 'photogallery/photogallery.html', context=context)


def get_photolist_days_archives(gallery):
    """ Сортировка фотографий по годам, агрегирование дней и архивов фотографий """
    photogallery_list_origin = gallery.objects.all().order_by('year')

    years = []
    for item in photogallery_list_origin:
        years.append(item.year)

    years = set(years)
    years = sorted(years, reverse=True)

    photogallery_list = []
    for year in years:
        photogallery_list.append([year, Gallery.objects.filter(year=year)])

    days = []
    for item in photogallery_list_origin:
        days.append(item.day)

    archives = []
    for item in photogallery_list_origin:
        archives.append(item.zipfile)

    days = set(days)
    days = sorted(days, reverse=False)

    return photogallery_list, days, archives
