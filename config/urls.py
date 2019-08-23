from django.contrib import admin
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('', include('chat.urls')),
]
