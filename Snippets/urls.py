from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('snippets/add', views.add_snippet_page, name='add-snippet'),
    path('snippets/list', views.snippets_page, name='view-snippet'),
    path('snippets/my', views.my_snippets, name='my-snippets'),
    path('snippets/<int:snippetId>', views.snippet_page, name='snippet-page'),
    path('snippets/<int:snippetId>/edit', views.snippet_edit, name='snippet-edit'),
    path('snippets/<int:snippetId>/delete', views.snippet_delete, name='snippet-delete'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    # path('snippets/create', views.create_snippet, name='snippet-create'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
