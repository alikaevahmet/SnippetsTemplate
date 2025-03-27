from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    # Создаем пустую форму при запросе GET
    if request.method == 'GET':
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)
    
    # Получаем данные из формы и создаем новый snippet в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
             form.save()
             return redirect('view-snippet') # GET /snippet_list/list
        return render(request, 'pages/add_snippet.html', {'form': form})
    



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
    else:
        context['snippet'] = snippet
        context['type'] = 'view'
    return render(request, 'pages/snippet_page.html', context)


def snippet_edit(request, snippetId):
    pass

def snippet_delete(request, snippetId):
    if request.method == "POST" or request.method == "GET":
        snippet = get_object_or_404(Snippet, id=snippetId)
        snippet.delete()
    return redirect('view-snippet')
