from django.http import Http404
from django.shortcuts import render, redirect
from .models import Snippet
from django.http import HttpResponseNotFound
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
        }
    return render(request, 'pages/view_snippets.html', context)

def snippet_page(request, snippetId):
    try:
        snippet = Snippet.objects.get(pk=snippetId)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Snippet with id={snippetId} not found')
    else:
        context = {
            'snippet': snippet,
            'pagename': 'Просмотр сниппета',
            }
    return render(request, 'pages/snippet_page.html', context)