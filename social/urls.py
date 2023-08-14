"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = 'PROTUBEWEB ADMIN'
admin.site.site_title = 'PROTUBEWEB ADMIN'
admin.site.index_title = 'WELCOME TO PROTUBEWEB ADMIN PANEL'
urlpatterns = [
    path('login/', admin.site.urls),
    path('logout/',RedirectView.as_view(url = '/admin/logout/')),
    path('root/',include('root.urls')),
    path('auth_system/',include('auth_system.urls')),
    path('chat/',include('chat.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  