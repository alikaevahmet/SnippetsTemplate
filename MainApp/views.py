from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required(login_url='index')
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
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect('view-snippet') # GET /snippet_list/list
        return render(request, 'pages/add_snippet.html', {'form': form})


@login_required(login_url='index')
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'snippets': snippets,
        'pagename': 'Мои сниппеты',
        'count': len(snippets),
        }
    return render(request, 'pages/view_snippets.html', context)


def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
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
        return render(request, context | {'error': f'Snippet with id={snippetId} not found'})
    else:
        context['snippet'] = snippet
        context['type'] = 'view'
    return render(request, 'pages/snippet_page.html', context)

@login_required
def snippet_edit(request, snippetId):
    context = {'pagename': 'Редактирование сниппета'}
    try:
        snippet = Snippet.objects.filter(user=request.user).get(pk=snippetId)
    except ObjectDoesNotExist:
        return Http404
    
    # Вариант 1
    # # Получение данных сниппета с помощью SnippetForm
    # if request.method == 'GET':
    #     form = SnippetForm(instance=snippet)
    #     return render(request, 'pages/add_snippet.html', {'form': form})


    # Вариант 2
    # Хотим получить страницу с данными сниппета
    if request.method == 'GET':
        form = SnippetForm()
        context['snippet'] = snippet
        context['type'] = 'edit'
        return render(request, 'pages/snippet_page.html', context)
    
    # Получаем данные из формы и создаем новый snippet в БД
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form['name']
        snippet.code = data_form['code']
        snippet.public = data_form.get('public', False)
        snippet.save()
        return redirect('view-snippet') # GET /snippet_list/list
@login_required
def snippet_delete(request, snippetId):    
    if request.method == "POST" or request.method == "GET":
        snippet = get_object_or_404(Snippet.objects.filter(user=request.user), id=snippetId)
        snippet.delete()
    return redirect('view-snippet')



def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                'pagename': 'PythonBin',
                'errors': ['wrong username or password'],
            }
            return render(request, 'pages/index.html', context)
    return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('index')