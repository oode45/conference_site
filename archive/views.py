from django.shortcuts import render
from archive.models import Archive


def archive_view(request):
    """" Сервис, который рендерит страницу с архивами докладов """
    context = {
        'arc_list': sorted_archive_list(Archive)
    }

    return render(request, 'archive/archive.html', context=context)


def sorted_archive_list(archive_model):
    """ Возвращает список архивов докладов, отсортированный по годам """
    archive_list_origin = archive_model.objects.all().order_by('-year')
    years = []
    for item in archive_list_origin:
        years.append(item.year)
    years = set(years)
    years = sorted(years, reverse=True)

    arc_list = []
    for year in years:
        arc_list.append([year, Archive.objects.filter(year=year)])
    
    return arc_list
