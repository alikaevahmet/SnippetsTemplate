from django.http import Http404
from django.shortcuts import render, redirect
from .models import Snippet
from django.core.exceptions import ObjectDoesNotExist

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'snippets': snippets,
        'pagename': 'Просмотр сниппетов',
        'count': len(snippets),
        }
    return render(request, 'pages/view_snippets.html', context)

def snippet_page(request, snippetId):
    context = {'pagename': 'Просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(pk=snippetId)
    except ObjectDoesNotExist:
        return render(request, 'pages/errors.html', context | {'error': f'Snippet with id={snippetId} not found'})
        # return HttpResponseNotFound(f'Snippet with id={snippetId} not found')
    else:
        context['snippet'] = snippet
    return render(request, 'pages/snippet_page.html', context)